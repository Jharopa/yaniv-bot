""" YanivBot """

import asyncio, os, random

import discord
from discord.ext import commands

from utils import config

CONFIGURATION = config.load()
DISCORD_TOKEN = CONFIGURATION['token']
COMMAND_PREFIX = CONFIGURATION['prefix']
UNIQUE_RESPONDEES = CONFIGURATION['unique_respondees']
RESPONSES = CONFIGURATION['responses']

intents=discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(COMMAND_PREFIX), intents=intents)

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} has connected')

@bot.event
async def on_message(message):
    if message.author.id in UNIQUE_RESPONDEES:
        await message.channel.send(random.choice(RESPONSES))

async def load_cogs() -> None:
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

def main():
    asyncio.run(load_cogs())
    
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
