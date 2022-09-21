from discord.ext import commands

from core import config, errors


def not_blacklisted():
    async def predicate(ctx: commands.Context) -> bool:
        blacklist = config.load()["blacklist"]
        if ctx.author.id in blacklist:
            raise errors.UserBlacklisted
        return True

    return commands.check(predicate)
