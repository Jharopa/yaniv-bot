""" YanivBot """

import asyncio
import os
import random

import discord
from discord.ext import commands

from yaniv_bot.core import config, errors

config = config.load()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

bot.config = config

message_logs = {}


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} has connected")


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return

    if message.author.id in bot.config["unique_respondees"]:
        await message.channel.send(random.choice(bot.config["responses"]))
        await bot.process_commands(message)

    if message.author.id in [276867841540489228]:
        message_logs.update({message.id: (message.content, message.attachments)})
    else:
        await bot.process_commands(message)


@bot.event
async def on_message_delete(message: discord.Message) -> None:
    if message.id in message_logs:
        await message.channel.send(f"{message.author.mention} just deleted a message")

        content = message_logs[message.id][0]
        attachments: list(discord.Attachment) = message_logs[message.id][1]

        if content:
            await message.channel.send(f"{content}")

        if attachments:
            for attachemnt in attachments:
                await message.channel.send(f"{attachemnt.url}")


@bot.event
async def on_command(ctx: commands.Context) -> None:
    return


@bot.event
async def on_command_completion(ctx: commands.Context) -> None:
    return


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, errors.UserBlacklisted):
        await ctx.channel.send(
            f"{ctx.author.mention} is blacklisted from running {bot.user.mention} commands on the server!"
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(
            f"{ctx.author.mention} is missing the permissions to run the {bot.user.mention} **{ctx.command}** command!"
        )
    elif isinstance(error, commands.errors.HybridCommandError):
        return
    else:
        raise error


@bot.event
async def on_member_join(member: discord.Member):
    return


async def load_cogs() -> None:
    for folder in os.listdir("./yaniv_bot/cogs"):
        for file in os.listdir(f"./yaniv_bot/cogs/{folder}"):
            if file.endswith(".py") and file not in []:
                await bot.load_extension(f"yaniv_bot.cogs.{folder}.{file[:-3]}")


def main() -> None:
    asyncio.run(load_cogs())

    bot.run(config["token"])


if __name__ == "__main__":
    main()
