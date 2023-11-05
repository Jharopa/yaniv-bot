import random

import discord
from discord.ext import commands

from yaniv_bot.core import checks


class Basic(commands.Cog, name="Basic Commands"):
    __slots__ = (
        "bot",
        "quotes",
    )

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.quotes: list[str] = []

    @commands.hybrid_command(
        name="quote",
        description="Use this command for a random qoute.",
        brief="What have we got to say today?",
    )
    @checks.not_blacklisted()
    async def qoute(self, ctx: commands.Context) -> None:
        await ctx.send(f'"{self.get_quote()}"')

    @qoute.error
    async def qoute_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            return

    def get_quote(self) -> str:
        if not self.quotes:
            self.load_quotes()

        return self.quotes.pop(-1)

    def load_quotes(self) -> list[str]:
        quotes = []

        with open("quotes.txt", "r", encoding="UTF-8") as f:
            quotes = [line.rstrip() for line in f]

        random.shuffle(quotes)

        self.quotes = quotes

    @commands.hybrid_command(
        name="about",
        description="Use this command for more information on Yaniv bot.",
        brief="Yaniv bot information",
    )
    @checks.not_blacklisted()
    async def about(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="YanivBot GitHub",
            url="https://github.com/Jharopa/yaniv-bot",
            description="Star, contribute, or just have a look around!",
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/app-icons/1019587025420173323/bcabb23a73df96956e63cba99891eace.png"
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="roll",
        description="Use this command to roll a number.",
        brief="Rolls you a number",
    )
    @checks.not_blacklisted()
    async def roll(self, ctx: commands.Context, frm: int = None, to: int = None):
        author = ctx.author

        if frm is None and to is None:
            await ctx.send(f":game_die: {random.randrange(1, 100)} :game_die:")
        elif frm is None:
            await ctx.send(f"{author.mention} From what to {to}?")
        elif to is None:
            await ctx.send(f"{author.mention} From {frm} to what?")
        elif frm < 0 or to < 0:
            await ctx.send(
                f"{author.mention} Maybe use some positive numbers ¯\\_(ツ)_/¯."
            )
        else:
            await ctx.send(f":game_die: {random.randrange(frm, to)} :game_die:")

    @roll.error
    async def roll_error(self, ctx: commands.Context, error: commands.CommandError):
        author = ctx.message.author

        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(
                f"{author.mention} Not sure what to do with that ¯\\_(ツ)_/¯ try using numbers."
            )


async def setup(bot):
    await bot.add_cog(Basic(bot))
