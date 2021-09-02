# Commands to archive a club

import discord
from setup_logger import logger
from discord.ext import commands
import re

class archive_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

################################################ BOT COMMANDS ##############################################
    @commands.command(name="archive_club", aliases=["archive", "ac"], brief = "Archive active club.", help = "Moves the club to archive category.")
    async def archive_club(self, ctx, group):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command archive club called")
        group = group.lower()

        if(bool(re.match(self.bot.conf["club_prefix"], group))):
            channel = discord.utils.get(ctx.guild.channels, name = group)
            category = discord.utils.get(ctx.guild.categories, name = self.bot.conf["archive_category"])

            if (channel != None):
                logger.info("archive channel " + channel.name)
                await channel.edit(category=category)
            await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        else:
            await ctx.message.add_reaction(self.bot.conf["emoji_nok"])


    @commands.command(name="respawn_club", aliases=["respawn", "res"], brief = "Respawn archived club.", help = "Moves the club back to clubs category.")
    async def respawn_club(self, ctx, group):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command respawn club called")
        group = group.lower()

        if(bool(re.match(self.bot.conf["club_prefix"], group))):
            channel = discord.utils.get(ctx.guild.channels, name = group)
            category = discord.utils.get(ctx.guild.categories, name = self.bot.conf["clubs_category"])

            if (channel != None):
                logger.info("respawn channel " + channel.name)
                await channel.edit(category=category)
            await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        else:
            await ctx.message.add_reaction(self.bot.conf["emoji_nok"])
def setup(bot):
    bot.add_cog(archive_helper(bot))