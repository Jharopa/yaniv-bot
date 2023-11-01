import discord
import requests
from discord.ext import commands

from yaniv_bot.core import checks


class Steam(commands.Cog, name="Steam Commands"):
    __slots__ = ("bot",)

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="steam",
        description="Use this command to receive a link to Yaniv's Steam, along with other related information.",
        brief="The legend's Steam account.",
    )
    @checks.not_blacklisted()
    async def steam_profile(self, ctx: commands.Context, *, steam_id) -> None:
        print(steam_id)

        steam_info = self.get_steam_info(steam_id)

        print(steam_info)

        embed = discord.Embed(
            title=steam_info["personaname"], url=steam_info["profileurl"]
        )

        embed.set_thumbnail(url=steam_info["avatar"])

        if "game" in steam_info:
            embed.add_field(
                name="Currently Playing",
                value=steam_info["game"],
                inline=False,
            )

        await ctx.send(embed=embed)

    @steam_profile.error
    async def steam_profile_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            return

    def get_steam_info(self, steam_id):
        with requests.Session() as session:
            summary = session.get(
                f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.bot.config["steam_api_key"]}&steamids={steam_id}'
            ).json()["response"]["players"][0]

            if "gameid" in summary:
                playing = session.get(
                    f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.bot.config["steam_api_key"]}&steamid={steam_id}&include_appinfo=true&include_played_free_games=true&appids_filter[0]={summary["gameid"]}'
                ).json()["response"]["games"][0]

            return {
                "personaname": summary["personaname"],
                "profileurl": summary["profileurl"],
                "avatar": summary["avatarfull"],
                "game": playing["name"],
                "game_img": f'http://media.steampowered.com/steamcommunity/public/images/apps/{playing["appid"]}/{playing["img_icon_url"]}.jpg',
            }


async def setup(bot):
    await bot.add_cog(Steam(bot))
