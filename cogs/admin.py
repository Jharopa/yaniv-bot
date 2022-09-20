import discord
from discord.ext import commands

class Admin(commands.Cog, name='Admin Commands'):
    __slots__ = (
        'bot',
    )

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        description='Use this command to kick a member of the discord server.',
        brief='Kick a server member.'
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if reason is None:
            reason = 'No reason provided.'

        await ctx.guild.kick(member)
        await ctx.send(f'User {member.mention} has been kick.')

async def setup(bot): 
    await bot.add_cog(Admin(bot))
