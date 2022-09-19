""" YanivBot """

import asyncio, os, random

import discord
from discord.ext import commands

from core import config

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
async def on_command(context: commands.Context):
    return

@bot.event
async def on_command_completion(context: commands.Context):
    return

@bot.event
async def on_command_error(context: commands.Context, error: commands.CommandError):
    return

async def load_cogs() -> None:
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

def main() -> None:
    asyncio.run(load_cogs())
    
    bot.run(config['token'])

if __name__ == "__main__":
    main()
