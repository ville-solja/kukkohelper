# General clubs commands
import discord
from setup_logger import logger
from discord.ext import commands
from discord.commands import SlashCommandGroup
import re
from datetime import datetime

class general_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.bot.conf["start_time"] = datetime.now()

    def uptime(self):
        seconds = (datetime.now() - self.bot.conf["start_time"]).total_seconds()
        hours = seconds / 3600
        minutes = (seconds / 60) % 60
        seconds = seconds % 60
        return '%0.2d:%02d:%02d' % (hours, minutes, seconds)

    general = SlashCommandGroup("general", "General bot commands for general use")

################################################ BOT COMMANDS ##############################################
    @general.command(name="ping", description="Test server latency.")
    async def ping(self, ctx):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command ping called")
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)} ms.")


    @general.command(name="print_stats", description = "Show interesting stats.")
    async def stats(self, ctx):
        self.bot.commands_called = self.bot.commands_called + 1
        message = "```\n"
        message += "Commands answered: " + str(self.bot.commands_called) + "\n"
        message += "Uptime: " + self.uptime()  + "\n"
        message += "```"

        logger.info("Stats called")
        await ctx.respond(message)


def setup(bot):
    bot.add_cog(general_helper(bot))