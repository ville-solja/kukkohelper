import os
import toml
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import re
import requests
from random import randint

## global variables
conf = dict()
secrets = dict()

############################################## DEFAULT SETTINGS ##############################################
## General
conf["bot_active"] = True
conf["settings_file"] = "/config/config.toml"
secrets["token"] = None

## Azure
conf["azurefilter"] = True
conf["emoji_checkmark"] = "✅"
secrets["azure_url_ext"] = None
secrets["azure_headers"] = None

## Logging
conf["log_level"] = 0 ## 0-5
conf["log_to_console"] = True
conf["log_to_channel"] = True
conf["log_channel"] = 869893210636451911
conf["logging_timestamp_format"] ="%Y%m%d %H:%M:%S"

## Bot
conf["command_prefix"] = "!"

############################################## END DEFAULT SETTINGS ##############################################

# Load environment variables
def load_env():
    global secrets
    secrets["token"] = os.environ["TOKEN"]
    secrets["azure_url_ext"] = os.environ["AZURE_URL_EXT"]
    secrets["azure_headers"] = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": os.environ["KEY"]}

# Load configuration from TOML file
async def loadConf(path):
    global conf

    configFile = path
    await log(1, "Trying to load configuration from: " + configFile, False)
    if(os.path.isfile(configFile)):
        conf = toml.load(configFile)
        await log(2, "Configuration loaded", False)
        await log(1, str(conf), False)
    else:
        await log(4, "Error loading configuration from file", False)

# Write current configuration to TOML file
async def writeConf(path):
    configFile = path
    global conf
    
    if(os.path.exists):
        f = open(configFile, "w")
        toml.dump(conf, f)
        await log(2, "Configuration saved to file: " + configFile)
    else:
        await log(5, "Cannot write configuration to file: " + configFile)

# logging function
async def log(level, message, log_to_channel=None):
    if(log_to_channel == None):
        log_to_channel = conf["log_to_channel"]
    timestamp = datetime.now().strftime(conf["logging_timestamp_format"])
    if(level >= conf["log_level"]):
        if(conf["log_to_console"] == True):
            print(timestamp + " " + message)
        
        if(log_to_channel == True):

            await send_message(conf["log_channel"], timestamp + " " +message)


async def send_message(channel_id, message):
    await bot.get_channel(channel_id).send(message)

def active():
    return (conf["bot_active"])

## Initialize
bot = commands.Bot(command_prefix=conf["command_prefix"])

############################################## BOT EVENTS ##############################################
## Initial status
@bot.event
async def on_ready():
        await log(2, f"{bot.user} online")

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
            await log(1, "Azure request: " + secrets["azure_url_ext"] + "\n" + str(json) + "\n" + str(secrets["azure_headers"]))

            tuomio = azure_request(secrets["azure_url_ext"], json, secrets["azure_headers"])
            if(tuomio is False):
                await message.add_reaction(conf["emoji_checkmark"])
                

            elif(tuomio == True and message.channel.is_nsfw() is False):
                    await message.delete()
                    msg = 'Image was deleted due to high Adultscore\nPlease repost to NSFW'
                    await log(2, "NSFW image deleted")
                    await message.channel.send(msg)
            else:
                await log(4, "Failed to fetch NFSW rating, status: " + tuomio)
                msg = "Could not get NSFW rating!"
                await message.channel.send(msg)
    await bot.process_commands(message)

def azure_request(azure_url, json, headers):
    response = requests.post(azure_url, json = json, headers = headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return str(response)
    return response.json()['adult']['isAdultContent']

############################################## END BOT EVENTS ##############################################

################################################ BOT COMMANDS ##############################################
@bot.command(name="ping", help = "Test if bot is online/active")
async def ping(ctx):
    await log(1, "command ping called")
    if(active()):
        await ctx.send("Pong! Bot functions online")
    else:
        await ctx.send("Bot functions currently offline.")

@bot.command(name="power_switch", help="Turn bot functions <on/off>.")
@commands.has_role('test-role')
async def power_switch(ctx, toggle):
    await log(2, "Command powerswitch called")
    global conf
    if(toggle == "on"):
        conf["bot_active"] = True
        await log(2, "Set bot_active = True")
        await ctx.send("Bot functions now active")
    elif(toggle == "off"):
        conf["bot_active"] = False
        await log(2, "Set bot_active = False")
        await ctx.send("Bot functions now inactive")
    else:
        await log(2, "Invalid argument supplied")
        await ctx.send("Invalid argument supplied, please use !active <on/off>")

@bot.command(name="nfsw_switch", help="Turn nfsw check <on/off>.")
@commands.has_role('test-role')
async def nsfw_switch(ctx, toggle):
    if(active()):
        await log(2, "Command nfsw_switch called")
        global conf
        if(toggle == "on"):
            conf["azurefilter"] = True
            await log(2, "set Azurefilter = True")
            await ctx.send("Nfsw filtering now active")
        elif(toggle == "off"):
            conf["azurefilter"] = False
            await log(2, "Set azurefilter = False")
            await ctx.send("Nfsw filtering now inactive")
        else:
            await log(2, "Invalid argument supplied")
            await ctx.send("Invalid argument supplied, please use !nfsw_switch <on/off>")

@bot.command(name="log_to_channel", brief="Set bot logging to dump to a specified channel.", help="Use !log_to_channel <channel_id> to enable. !log_to_channel <off> to disable.")
@commands.has_role('test-role')
async def log_to_channel(ctx, command):
    global conf
    if(active()):
        await log(2, "command set_log_to_channel called")
        if(command == "off"):
            await log(2, "Turning off logging to channel...")
            conf["log_to_channel"] = False
            await log(2, "Logging to channel turned off.")
            await ctx.send("OK, check log")
        else:
            guild = ctx.guild
            channel = discord.utils.get(guild.text_channels, name = command)
            if (channel is not None):
                await log(1, "Previous logging channel was: " + str(conf["log_channel"]))
                await log(2, "Setting new logging channel to: " + str(channel.id))
                conf["log_channel"] = channel.id
                conf["log_to_channel"] = True
                await ctx.send("OK, check log")

@bot.command(name="wrmem", brief="Save bot configuration to permanent storage.")
@commands.has_role('test-role')
async def wrmem(ctx):
    if(active()):
        await log(2, "command wrmem called")
        await writeConf(conf["settings_file"])

@bot.command(name="loadConfig", brief="Load bot configuration from permanent storage.")
@commands.has_role('test-role')
async def loadConfig(ctx):
    if(active()):
        await log(2, "command loadConfig called")
        await loadConfig(conf["settings_file"])

@bot.command(name="join", brief = "Join a group.", help = "Join a gaming group. Group/Role name is case sensitive!!")
async def join(ctx, group):
    if(active()):
        await log(2, "command join called")
        member = ctx.message.author

        is_game = bool(re.match("game",group,  re.IGNORECASE))

        if(is_game):
            role = discord.utils.get(ctx.guild.roles, name = group)
            if (role == None):
                await ctx.send("Group not found. Please note that group name is case sensitive.")
                await log(2, "Group " + group + " not found on server.")
            else:
                await member.add_roles(role)
                await log(2, "Added " + str(ctx.message.author) + " to group " + str(role))
                await ctx.send("I added you to group " + str(role))
        else:
            await ctx.send("You can only add groups with Game- prefix currently.")

@bot.command(name="quit", brief= "Leave a group.", help = "Leave a gaming group. Group/Role name is canse sensitive!!")
async def quit(ctx, group):
    if(active()):
        await log (2, "command quit called")
        member = ctx.message.author

        role = discord.utils.get(ctx.guild.roles, name = group)
        if(role in member.roles):
            await member.remove_roles(role)
            await log(2, "Deleted role " + str(role) + " from " + str(member))
            await ctx.send("I removed you from " + str(role))
        else:
            await log(2, "Role " + str(role) + " not found for user " + str(member))
            await ctx.send("Could not find you in " + group)

@bot.command(name="list", brief = "List gaming groups.")
async def list(ctx):
    if(active()):
        await log (2, "command list called")
        roles = ctx.guild.roles
        message = "```\n"

        for role in roles:
            if(bool(re.match("game", str(role),  re.IGNORECASE))):
                message = message + str(role) + "\n"
        message = message + "```"
        await log(1, message, False)
        await ctx.send(message)

@bot.command(name="dota_random", brief = "Use to pick a random hero for dota.")
async def dota_random(ctx):
    if(active()):
        await log(2, "command dota random called")
        response = requests.get("https://api.opendota.com/api/heroes/")
        rand = randint(1, len(response.json()))
        msg = """You're going to play {0} a {1} hero with {2} legs""".format(response.json()[rand]["localized_name"], response.json()[rand]["primary_attr"], response.json()[rand]["legs"])
        await ctx.send(msg)

############################################## END BOT COMMANDS ##############################################

## Run
load_env()
print(secrets["token"])
bot.run(secrets["token"])
