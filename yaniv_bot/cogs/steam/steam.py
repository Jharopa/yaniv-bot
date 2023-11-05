import aiohttp
import discord
from discord.ext import commands

from yaniv_bot.core import checks


class Steam(commands.Cog, name="Steam Commands"):
    __slots__ = ("bot", "api_key")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.api_key = self.bot.config["steam_api_key"]

    @commands.hybrid_command(
        name="steam",
        description="Use this command to receive a link to Yaniv's Steam, along with other related information.",
        brief="The legend's Steam account.",
    )
    @checks.not_blacklisted()
    async def steam_profile(self, ctx: commands.Context, *, steam_id) -> None:
        steam_info = await self.get_steam_info(steam_id)

        if steam_info:
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
        else:
            embed = discord.Embed(
                title="Error!",
                description="Something went wrong with the Steam API, please try again later",
                color=0xE02B2B,
            )

            await ctx.send(embed=embed)

    @steam_profile.error
    async def steam_profile_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Error!",
                description="Non-existent Steam ID provided",
                color=0xE02B2B,
            )

            await ctx.send(embed=embed)
        else:
            raise error

    async def get_steam_info(self, steam_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.api_key}&steamids={steam_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    if data["response"]["players"]:
                        summary = data["response"]["players"][0]

                        steam_info = {
                            "personaname": summary["personaname"],
                            "profileurl": summary["profileurl"],
                            "avatar": summary["avatarfull"],
                        }
                    else:
                        raise commands.errors.BadArgument
                else:
                    return None

                if "gameid" in summary:
                    game_info = await self.get_game_info(steam_id, summary["gameid"])

                    if game_info:
                        steam_info.update(game_info)

        return steam_info

    async def get_game_info(self, steam_id, game_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.api_key}&steamid={steam_id}&include_appinfo=true&include_played_free_games=true&appids_filter[0]={game_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    playing = data["response"]["games"][0]

                    return {
                        "game": playing["name"],
                        "game_img": f'http://media.steampowered.com/steamcommunity/public/images/apps/{playing["appid"]}/{playing["img_icon_url"]}.jpg',
                    }
                else:
                    return None


async def setup(bot):
    await bot.add_cog(Steam(bot))
