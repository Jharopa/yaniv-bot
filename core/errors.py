from discord.ext import commands


class UserBlacklisted(commands.CheckFailure):
    def __init__(self, message: str = "User is blacklisted") -> None:
        super().__init__(message)
