from discord.ext import commands

from core import config

def not_blacklisted():
    async def predicate(context: commands.Context) -> bool:
        blacklist = config.load()['blacklist']
        return not context.author.id in blacklist

    return commands.check(predicate)
