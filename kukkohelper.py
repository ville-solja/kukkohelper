import os
from discord.ext import commands
from random import randint
from setup_logger import logger

## global variables
default_conf = dict()
conf = dict()
commands_called = 0

############################################## DEFAULT SETTINGS ##############################################
## General
default_conf["token"] = None

## Azure
default_conf["azurefilter"] = False
default_conf["emoji_ok"] = "✅"
default_conf["emoji_nok"] = "❌"
default_conf["azure_url_ext"] = None
default_conf["azure_key"] = None

## Bot
default_conf["command_prefix"] = "!"
default_conf["initial_extensions"] = ["general", "dota", "archive", "nsfw", "stats"]
default_conf["clubs_category"] = "CLUBS"
default_conf["archive_category"] = "ARCHIVE"
default_conf["club_prefix"] = "club-"

############################################## END DEFAULT SETTINGS ##############################################

# Load environment variables
def load_env():
    global conf
    global default_conf
    conf = default_conf | os.environ
    print(conf)

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

############################################## END BOT EVENTS ##############################################

## Run
bot.conf = dict()
bot.conf = conf
bot.commands_called = commands_called
for ext in conf["initial_extensions"]:
    bot.load_extension(ext)
bot.run(conf["token"])