# nsfw filter
import discord
from setup_logger import logger
from discord.ext import commands
import requests

class nsfw_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def azure_request(self, azure_url, json, key):
        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["Ocp-Apim-Subscription-Key"] = key
        response = requests.post(azure_url, json = json, headers = headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return str(response)
        return response.json()['adult']['isAdultContent']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if(self.bot.conf["azurefilter"] == True):
            if len(message.attachments) > 0:
                json = {'url': '{0}'.format(message.attachments[0].url)}
                logger.info("Azure request: " + self.bot.conf["azure_url_ext"] + "\n" + str(json) + "\n" + str(self.bot.conf["azure_key"]))

                tuomio = self.azure_request(self.bot.conf["azure_url_ext"], json, self.bot.conf["azure_key"])
                if(tuomio is False):
                    await message.add_reaction(self.bot.conf["emoji_ok"])

                elif(tuomio == True and message.channel.is_nsfw() is False):
                        await message.delete()
                        msg = 'Image was deleted due to high Adultscore\nPlease repost to NSFW'
                        logger.info("NSFW image deleted")
                        await message.channel.send(msg)
                else:
                    logger.warning("Failed to fetch NFSW rating, status: " + tuomio)
                    await message.add_reaction(self.bot.conf["emoji_nok"])

################################################ BOT COMMANDS ##############################################
    @commands.command(name="nsfw_filter", brief = "Turn nfsw check <on/off>.", help="Turn nfsw check <on/off>. Azure key and address need to be configured for filter to work!")
    @commands.has_guild_permissions(administrator=True)
    async def nsfw_switch(self, ctx, toggle):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("Command nfsw_switch called")
        if(toggle == "on"):
            self.bot.conf["azurefilter"] = True
            logger.info("set Azurefilter = True")
            await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        elif(toggle == "off"):
            self.bot.conf["azurefilter"] = False
            logger.info("Set azurefilter = False")
            await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        else:
            logger.info("Invalid argument supplied")
            await ctx.message.add_reaction(self.bot.conf["emoji_nok"])

############################################## END BOT COMMANDS ##############################################



def setup(bot):
    bot.add_cog(nsfw_helper(bot))