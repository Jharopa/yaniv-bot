""" YanivBot """

import os, random

import discord

from utils import config

DISCORD_TOKEN = config.load()['token']
COMMAND_PREFIX = config.load()['prefix']

class CustomClient(discord.Client):
    def __init__(self):
        self.quotes = []

        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        print(f'{self.user} has connected')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content[0] != COMMAND_PREFIX:
            return

        if message.content == '!yq':
            quote = self.get_quote()
            await message.channel.send(f'"{quote}" - __Yaniv__ <:Yshit:824266966775889931>')
        elif message.content == '!yw':
            await message.channel.send('https://yanivboost.com/')

    def get_quote(self) -> str:
        if not self.quotes:
            self.load_quotes()

        return self.quotes.pop(-1)
    
    def load_quotes(self):
        quotes = []

        with open('quotes.txt', 'r', encoding='UTF-8') as f:
                quotes = [line.rstrip() for line in f]

        random.shuffle(quotes)

        self.quotes = quotes

def main():
    client = CustomClient()
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
