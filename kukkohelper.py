import discord
import requests
import sys
import datetime
from random import randint
from RepeatedTimer import RepeatedTimer

TOKEN = open('TOKEN', 'r').read().strip()
KEY = open('KEY', 'r').read().strip()

emoji_checkmark = '✅'
azure_url_ext = "https://northeurope.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=adult"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": KEY
}
client = discord.Client()
global streamers
streamers = {}
list_of_songs = []

def user_recently_announced(name):
    if name in streamers:
        print("name found in list, do additional steps")
        return True
    else:
        print("name not found in list")
        now = datetime.datetime.now()
        add_to_list(name, now)
        return False


def add_to_list(name, now):
    print("streamer added: {0}".format(name))
    streamers.update({name: {"time": now}})


def prune_list(streamers):
    print("prune_list called")
    print(streamers)
    for name, value in streamers.items():
        print(name)
        print(value)
        print(value["time"])
        compare = (datetime.datetime.now() - value["time"]).total_seconds()
        if compare > 3600:
            print("Will prune user {0} from list".format(name))
            try:
                del streamers[name]
            except RuntimeError:
                pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for guild in client.guilds:
        print(guild.name)
    
@client.event
async def on_member_update(before, after):
    print(after.activity)
    for activity in after.activities:
        if activity.type == discord.ActivityType.streaming:
            for role in after.roles:
                if role.name == 'Role-Streamer':
                    print('{} passed to user_recently_announced'.format(after))
                    if user_recently_announced(after.name) is False:
                        public_msg = '{0} presents: "{1}"! <{2}>'.format(after.name, activity.name, activity.url)
                        general = discord.utils.get(after.guild.channels, name='general')
                        await general.send(public_msg)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if len(message.attachments) > 0:
        data = {'url': '{0}'.format(message.attachments[0].url)}
        r = requests.post(azure_url_ext, json=data, headers=headers)
        nsfwchannel = discord.utils.get(message.guild.channels, name='nsfw')
        origchannel = message.channel
        if r.json()['adult']['isAdultContent'] is True:
            if origchannel is not nsfwchannel:
                await message.delete()
                msg = 'Image was deleted due to Adultscore: {0}.\nPlease repost to NSFW'.format(r.json()['adult']['adultScore'])
                await origchannel.send(msg)
        else:
            await message.add_reaction(emoji_checkmark)

    if message.content.startswith('!help'):
        msg = """This bot will help you find people to play games with!
        Commands:
        "!help" displays this message
        "!list" shows all available games
        "!add <role>" adds you to chosen role
        "!remove <role>" removes role if you have it
        "!dota random" picks a random dota hero
        """
        await message.author.send(msg)

    if message.content.startswith('!list'):
        l = 'Here is a list of game roles:\n'
        for s in client.guilds:
            for r in s.roles:
                if r.name.startswith('Game-'):
                    l += '{0}\n'.format(r.name[5:])
        l += '\nAnd here is a list of other roles:\n'
        for s in client.guilds:
            for r in s.roles:
                if r.name.startswith('Role-'):
                    l += '{0}\n'.format(r.name[5:])
        await message.author.send(l)

    if message.content.startswith('!add'):
        flag = False
        member = message.author
        if message.channel.type == discord.ChannelType.text:
            for guild in client.guilds:
                for role in guild.roles:
                    if role.name.startswith('Game-'):
                        if str(role.name[5:]).lower() == str(message.content[5:]).lower():
                            if discord.utils.get(member.roles, id=role.id) is not None:
                                msg = 'You already have that role!'
                                await message.channel.send(msg)
                                flag = True
                            else:
                                await member.add_roles(role)
                                await message.add_reaction(emoji_checkmark)
                                flag = True
                    if role.name.startswith('Role-'):
                        if str(role.name[5:]).lower() == str(message.content[5:]).lower():
                            if discord.utils.get(member.roles, id=role.id) is not None:
                                msg = 'You already have that role!'
                                await message.channel.send(msg)
                                flag = True
                            else:
                                await member.add_roles(role)
                                await message.add_reaction(emoji_checkmark)
                                flag = True
            if flag is False:
                msg = 'Something went wrong :shrug:'
                await message.channel.send(msg)
        else:
            msg = 'Add/Remove only function on public text channels'
            await message.author.send(msg)

    if message.content.startswith('!remove'):
        flag = False
        member = message.author
        if message.channel.type == discord.ChannelType.text:
            for guild in client.guilds:
                for role in guild.roles:
                    if role.name.startswith('Game-'):
                        if str(role.name[5:]).lower() == str(message.content[8:]).lower():
                            if discord.utils.get(member.roles, id=role.id) is not None:
                                await member.remove_roles(role)
                                await message.add_reaction(emoji_checkmark)
                                flag = True
                            else:
                                msg = "You don't have that role!"
                                await message.channel.send(msg)
                                flag = True
                    if role.name.startswith('Role-'):
                        if str(role.name[5:]).lower() == str(message.content[8:]).lower():
                            if discord.utils.get(member.roles, id=role.id) is not None:
                                await member.remove_roles(role)
                                await message.add_reaction(emoji_checkmark)
                                flag = True
                            else:
                                msg = "You don't have that role!"
                                await message.channel.send(msg)
                                flag = True
            if flag is False:
                msg = 'Something went wrong :shrug:'
                await message.channel.send(msg)
        else:
            msg = 'Add/Remove only function on public text channels'
            await message.author.send(msg)

    if message.content.startswith('!dota random'):
        r = requests.get('https://api.opendota.com/api/heroes/')
        rand = randint(1, len(r.json()))
        msg = """You're going to play {0} a {1} hero with {2} legs""".format(r.json()[rand]["localized_name"],
                                                                             r.json()[rand]["primary_attr"],
                                                                             r.json()[rand]["legs"])
        await message.channel.send(msg)

client.run(TOKEN)
