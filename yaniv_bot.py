""" YanivBot """

from http import client
import os, random

import discord
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

class CustomClient(discord.Client):
    def __init__(self):
        self.quotes = []

        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'{self.user} has connected')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$yq'):
            quote = self.get_quote()
            await message.channel.send(f'"{quote}" - __Yaniv__ <:Yshit:824266966775889931>')
        elif message.content.startswith('$yw'):
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
