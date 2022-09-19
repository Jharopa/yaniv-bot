from discord.ext import commands

from utils import config

def not_blacklisted():
    async def predicate(context: commands.Context) -> bool:
        blacklist = config.load()['blacklist']
        return not context.author.id in blacklist

    return commands.check(predicate)
