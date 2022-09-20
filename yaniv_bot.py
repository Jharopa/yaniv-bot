""" YanivBot """

import asyncio, os, random
from tkinter.messagebox import NO

import discord
from discord.ext import commands

from core import config, errors

config = config.load()

intents=discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config['prefix']), intents=intents)

bot.config = config

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} has connected')

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return

    if message.author.id in bot.config['unique_respondees']:
        await message.channel.send(random.choice(bot.config['responses']))
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
        await ctx.send(f'{ctx.author.mention} is blacklisted from running {bot.user.mention} commands!')
    else:
        raise error

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(config['notification_channel'])
    await channel.send(f'{member.mention} has joined the server!')

async def load_cogs() -> None:
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

def main() -> None:
    asyncio.run(load_cogs())
    
    bot.run(config['token'])

if __name__ == "__main__":
    main()
