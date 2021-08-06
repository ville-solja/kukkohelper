##from kukkohelper import active
import discord
from setup_logger import logger
from discord.ext import commands
import requests
from random import randint

class dota_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="dota_random", brief = "Use to pick a random hero for dota.")
    async def dota_random(self, ctx):
            logger.info("command dota random called")
            response = requests.get("https://api.opendota.com/api/heroes/")
            rand = randint(1, len(response.json()))
            msg = """You're going to play {0} a {1} hero with {2} legs""".format(response.json()[rand]["localized_name"], response.json()[rand]["primary_attr"], response.json()[rand]["legs"])
            await ctx.send(msg)
def setup(bot):
    bot.add_cog(dota_helper(bot))