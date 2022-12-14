""" YanivBot """

import asyncio
import os
import random

import discord
from discord.ext import commands

from yaniv_bot.core import config, errors

config = config.load()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents
)

bot.config = config


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} has connected")
    await bot.tree.sync()


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return

    if message.author.id in bot.config["unique_respondees"]:
        await message.channel.send(random.choice(bot.config["responses"]))
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)


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
    for file in os.listdir("./yaniv_bot/cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"yaniv_bot.cogs.{file[:-3]}")


def main() -> None:
    asyncio.run(load_cogs())

    bot.run(config["token"])


if __name__ == "__main__":
    main()
