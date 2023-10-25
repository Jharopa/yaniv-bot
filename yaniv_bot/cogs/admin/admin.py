from discord.ext import commands


class Admin(commands.Cog, name="Admin Commands"):
    __slots__ = ("bot",)

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        description="Use this command to kick a member of the discord server.",
        brief="Kicks a server member.",
    )
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: commands.MemberConverter,
        *,
        reason: str = "Not specified.",
    ):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"User {member.mention} has been kicked. Reason: {reason}")

    @commands.hybrid_command(
        description="Use this command to ban a member of the discord server.",
        brief="Bans a server member.",
    )
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: commands.MemberConverter,
        *,
        reason: str = "Not specified.",
    ):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"User {member.mention} has been banned. Reason: {reason}")

    @commands.hybrid_command(
        description="Use this command to disconnect a member of the discord server.",
        brief="Disconnects a server member",
    )
    @commands.has_permissions(kick_members=True)
    async def disconnect(
        self,
        ctx: commands.Context,
        member: commands.MemberConverter,
        *,
        reason: str = "Not specified.",
    ):
        try:
            channel = member.voice.channel

            if channel:
                await member.move_to(None)
                await ctx.send(
                    f"User {member.mention} has been disconnected. Reason: {reason}"
                )
        except AttributeError:
            await ctx.send(f"User {member.mention} is already disconnected.")


async def setup(bot):
    await bot.add_cog(Admin(bot))
