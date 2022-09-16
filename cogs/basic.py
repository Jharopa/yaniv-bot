import random

from discord.ext import commands

class basic(commands.Cog, name='Basic Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = []

    @commands.command(
        name='yw',
        description='Use this command for a link to the G.O.A.T of all sites',
        brief='The legend\'s own site'
    )
    async def website(self, ctx):
        await ctx.send('https://yanivboost.com/');

    @commands.command(
        name='yq',
        description='Use this command for a random, classic Yaniv qoute',
        brief='What has he got to say today?'
    )
    async def qoute(self, ctx):
        await ctx.send(f'"{self.get_quote()}" - __Yaniv__ <:Yshit:824266966775889931>');

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

async def setup(bot): 
    await bot.add_cog(basic(bot))
