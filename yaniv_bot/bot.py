import os
import random

import discord
from discord.ext import commands

from yaniv_bot.core import config, errors

config = config.load()

intents = discord.Intents.all()


class YanivBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=intents)

        self.config = config
        self.channel = None
        self.message_logs = {}

    async def load_cogs(self) -> None:
        for folder in os.listdir("./yaniv_bot/cogs"):
            for file in os.listdir(f"./yaniv_bot/cogs/{folder}"):
                if file.endswith(".py") and file not in []:
                    await self.load_extension(f"yaniv_bot.cogs.{folder}.{file[:-3]}")

    async def setup_hook(self) -> None:
        await self.load_cogs()

    async def on_guild_join(self, guild: discord.Guild):
        self.channel = discord.utils.get(guild.text_channels, name="yaniv-bot")

        if not self.channel:
            self.channel = await guild.create_text_channel("yaniv-bot")
            self.channel = await self.channel.set_permissions(
                guild.default_role, send_messages=False
            )

    async def on_ready(self) -> None:
        print(f"{self.user} has connected")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return

        if message.author.id in self.config["unique_respondees"]:
            await message.channel.send(random.choice(self.config["responses"]))

        if message.author.id in self.config["anti_deletion_users"]:
            self.message_logs.update(
                {message.id: (message.content, message.attachments, message.stickers)}
            )

        await self.process_commands(message)

    async def on_message_delete(self, message: discord.Message) -> None:
        if message.id in self.message_logs:
            await message.channel.send(
                f"{message.author.mention} just deleted a message"
            )

            content = self.message_logs[message.id][0]
            attachments: list(discord.Attachment) = self.message_logs[message.id][1]
            stickers: list(discord.StickerItem) = self.message_logs[message.id][2]

            if content:
                await message.channel.send(f"{content}")

            if attachments:
                for attachemnt in attachments:
                    await message.channel.send(f"{attachemnt.url}")

            if stickers:
                try:
                    await message.channel.send(stickers=stickers)
                except discord.errors.Forbidden:
                    await message.channel.send(
                        "It had a standard sticker in it, YanivBot can't send those :pensive:\nhttps://github.com/discord/discord-api-docs/issues/6399"
                    )

    async def on_command(self, ctx: commands.Context) -> None:
        return

    async def on_command_completion(self, ctx: commands.Context) -> None:
        return

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, errors.UserBlacklisted):
            await ctx.channel.send(
                f"{ctx.author.mention} is blacklisted from running {self.user.mention} commands on the server!"
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(
                f"{ctx.author.mention} is missing the permissions to run the {self.user.mention} **{ctx.command}** command!"
            )
        elif isinstance(error, commands.errors.HybridCommandError):
            return
        else:
            raise error

    async def on_member_join(self, member: discord.Member):
        return
