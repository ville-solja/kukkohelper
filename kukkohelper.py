import os
from discord.ext import commands
from datetime import datetime
import requests
from random import randint
from setup_logger import logger

## global variables
conf = dict()
secrets = dict()

############################################## DEFAULT SETTINGS ##############################################
## General
conf["settings_file"] = "/config/config.toml"
secrets["token"] = None

## Azure
conf["azurefilter"] = True
conf["emoji_checkmark"] = "✅"
secrets["azure_url_ext"] = None
secrets["azure_headers"] = None

## Bot
conf["command_prefix"] = "!"
conf["initial_extensions"] = ["cock-user", "dota"]

############################################## END DEFAULT SETTINGS ##############################################

# Load environment variables
def load_env():
    global secrets
    global conf
    if("TOKEN" in os.environ):
        secrets["token"] = os.environ["TOKEN"]
    if("AZURE_URL_EXT" in os.environ):
        secrets["azure_url_ext"] = os.environ["AZURE_URL_EXT"]
    if("KEY" in os.environ):
        secrets["azure_headers"] = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": os.environ["KEY"]}
    if("COMMAND_PREFIX" in os.environ):
        conf["command_prefix"] = os.environ["COMMAND_PREFIX"]

def azure_request(azure_url, json, headers):
    response = requests.post(azure_url, json = json, headers = headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return str(response)
    return response.json()['adult']['isAdultContent']

## Initialize
load_env()
bot = commands.Bot(command_prefix=conf["command_prefix"])

############################################## BOT EVENTS ##############################################
## Initial status
@bot.event
async def on_ready():
        logger.info(f"{bot.user} online")

## Error handling
@bot.event
async def on_command_error(ctx, error):
    if(isinstance(error, commands.errors.MissingRole)):
        await ctx.send("You do not have enough privileges to use this command.")
        return
    raise error

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if(conf["azurefilter"] == True):
        if len(message.attachments) > 0:
            json = {'url': '{0}'.format(message.attachments[0].url)}
            logger.debug("Azure request: " + secrets["azure_url_ext"] + "\n" + str(json) + "\n" + str(secrets["azure_headers"]))

            tuomio = azure_request(secrets["azure_url_ext"], json, secrets["azure_headers"])
            if(tuomio is False):
                await message.add_reaction(conf["emoji_checkmark"])
                

            elif(tuomio == True and message.channel.is_nsfw() is False):
                    await message.delete()
                    msg = 'Image was deleted due to high Adultscore\nPlease repost to NSFW'
                    logger.info("NSFW image deleted")
                    await message.channel.send(msg)
            else:
                logger.warning("Failed to fetch NFSW rating, status: " + tuomio)
                msg = "Could not get NSFW rating!"
                await message.channel.send(msg)
    await bot.process_commands(message)

############################################## END BOT EVENTS ##############################################

################################################ BOT COMMANDS ##############################################
@bot.command(name="nfsw_switch", help="Turn nfsw check <on/off>.")
async def nsfw_switch(ctx, toggle):
    logger.info("Command nfsw_switch called")
    global conf
    if(toggle == "on"):
        conf["azurefilter"] = True
        logger.info("set Azurefilter = True")
        await ctx.send("Nfsw filtering now active")
    elif(toggle == "off"):
        conf["azurefilter"] = False
        logger.info("Set azurefilter = False")
        await ctx.send("Nfsw filtering now inactive")
    else:
        logger.info("Invalid argument supplied")
        await ctx.send("Invalid argument supplied, please use !nfsw_switch <on/off>")

############################################## END BOT COMMANDS ##############################################

## Run
for ext in conf["initial_extensions"]:
    bot.load_extension(ext)
bot.run(secrets["token"])