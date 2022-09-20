import discord
from discord.ext import commands

import requests

from core import checks

class Steam(commands.Cog, name='Steam Commands'):
    __slots__ = (
        'bot',
    )

    def __init__(self, bot: commands.Bot) -> None:
        self.bot : commands.Bot = bot
    
    @commands.hybrid_command(
        name='ys',
        description='Use this command to receive a link to Yaniv\'s Steam, along with other related information.',
        brief='The legend\'s Steam account.'
    )
    @checks.not_blacklisted()
    async def steam_profile(self, ctx: commands.Context) -> None:
        with requests.Session() as session:
            user_stats = session.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.bot.config["steam_api_key"]}&steamids={self.bot.config["steam_id"]}').json()['response']['players'][0]

            embed = discord.Embed(
                title=user_stats['personaname'],
                url=user_stats['profileurl']
            )

            embed.set_thumbnail(url=user_stats['avatarfull'])
            embed.add_field(name='A.K.A', value=user_stats['realname'], inline=False)

            if 'gameid' in user_stats:
                currently_playing = session.get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.bot.config["steam_api_key"]}&steamid={self.bot.config["steam_id"]}&include_appinfo=true&include_played_free_games=true&appids_filter[0]={user_stats["gameid"]}').json()['response']['games'][0]
                embed.add_field(name='Currently Playing', value=currently_playing['name'], inline=False)
                embed.set_image(url=f'http://media.steampowered.com/steamcommunity/public/images/apps/{currently_playing["appid"]}/{currently_playing["img_icon_url"]}.jpg')

            await ctx.send(embed=embed)

    @steam_profile.error
    async def steam_profile_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CheckFailure):
            return

async def setup(bot): 
    await bot.add_cog(Steam(bot))
