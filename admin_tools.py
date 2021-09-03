# Commands for admins
import discord
from setup_logger import logger
from discord.ext import commands

class admin_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None



def setup(bot):
    bot.add_cog(admin_helper(bot))