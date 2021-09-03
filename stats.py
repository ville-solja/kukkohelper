# Commands to see bot stats
from setup_logger import logger
from discord.ext import commands
from datetime import datetime

class stats_helper(commands.Cog):
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
        

    @commands.command(name="bot_stats", aliases = ["stats"], brief = "Show interesting stats.")
    async def stats(self, ctx):
        self.bot.commands_called = self.bot.commands_called + 1
        message = "```\n"
        message += "Commands answered: " + str(self.bot.commands_called) + "\n"
        message += "Uptime: " + self.uptime()  + "\n"
        message += "```"

        logger.info("Stats called")
        await ctx.send(message)

def setup(bot):
    bot.add_cog(stats_helper(bot))