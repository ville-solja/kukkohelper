import discord
import requests
import platform
import sys
import random
from random import randint

TOKEN = open('TOKEN', 'r').read().strip()
KEY = open('KEY', 'r').read().strip()
LOG = open('errors.log', 'w')

emoji_checkmark = '✅'
emoji_stop = '🛑'
emoji_thumbup = '👍'
emoji_thumbdown = '👎'

azure_url_ext = "https://northeurope.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=categories,tags,description,adult"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": KEY
}
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for each in client.servers:
        print(each.name)

@client.event
async def on_member_update(before, after):
    if before.game.type is not 1:
        if after.game.type is 1:
            for role in after.roles:
                if role.name == 'Role-Streamer':
                    msg = '{0} presents: "{1}"! <{2}>'.format(after, after.game.name, after.game.url)
                    general = discord.utils.get(after.server.channels, name='general')
                    await client.send_message(general, msg)

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if len(message.attachments) > 0:
            data = {'url': '{0}'.format(message.attachments[0]['url'])}
            r = requests.post(azure_url_ext, json=data, headers=headers)
            nsfwchannel = discord.utils.get(message.server.channels, name='nsfw')
            origchannel = message.channel
            if r.json()['adult']['isAdultContent'] is True:
                if origchannel is not nsfwchannel:
                    await client.delete_message(message)
                    msg = 'Image was deleted due to Adultscore: {0}.\nPlease repost to NSFW'.format(r.json()['adult']['adultScore'])
                    await client.send_message(origchannel, msg)
            else:
                await client.add_reaction(message, emoji_checkmark)

        if message.content.startswith('!help'):
            msg = """This bot will help you find people to play games with!
            Commands:
            "!help" displays this message
            "!list" shows all available games
            "!add <role>" adds you to chosen role
            "!remove <role>" removes role if you have it
            "!dota random" picks a random dota hero
            "!git" posts a link to the bots source
            """
            await client.send_message(message.channel, msg)

        if message.content.startswith('!list'):
            l = 'Here is a list of game roles:\n'
            for s in client.servers:
                for r in s.roles:
                    if r.name.startswith('Game-'):
                        l += '{0}\n'.format(r.name[5:])
            l += '\nAnd here is a list of other roles:\n'   
            for s in client.servers:
                for r in s.roles:
                    if r.name.startswith('Role-'):
                        l += '{0}\n'.format(r.name[5:])
            await client.send_message(message.channel, l)

        if message.content.startswith('!add'):
            flag = False
            user = message.author
            for server in client.servers:
                for role in server.roles:
                    if role.name.startswith('Game-'):
                        if str(role.name[5:]).lower() == str(message.content[5:]).lower():
                            if discord.utils.get(user.roles, id=role.id) is not None:
                                msg = 'You already have that role!'
                                await client.send_message(message.channel, msg)
                                flag = True
                            else:
                                await client.add_roles(user, role)
                                await client.add_reaction(message, emoji_checkmark)
                                flag = True
                    if role.name.startswith('Role-'):
                        if str(role.name[5:]).lower() == str(message.content[5:]).lower():
                            if discord.utils.get(user.roles, id=role.id) is not None:
                                msg = 'You already have that role!'
                                await client.send_message(message.channel, msg)
                                flag = True
                            else:
                                await client.add_roles(user, role)
                                await client.add_reaction(message, emoji_checkmark)
                                flag = True
            if flag is False:
                msg = 'Something went wrong :shrug:'
                await client.send_message(message.channel, msg)

        if message.content.startswith('!remove'):
            flag = False
            user = message.author
            for server in client.servers:
                for role in server.roles:
                    if role.name.startswith('Game-'):
                        if str(role.name[5:]).lower() == str(message.content[8:]).lower():
                            if discord.utils.get(user.roles, id=role.id) is not None:
                                await client.remove_roles(user, role)
                                await client.add_reaction(message, emoji_checkmark)
                                flag = True
                            else:
                                msg = "You don't have that role!"
                                await client.send_message(message.channel, msg)
                                flag = True
                    if role.name.startswith('Role-'):
                        if str(role.name[5:]).lower() == str(message.content[8:]).lower():
                            if discord.utils.get(user.roles, id=role.id) is not None:
                                await client.remove_roles(user, role)
                                await client.add_reaction(message, emoji_checkmark)
                                flag = True
                            else:
                                msg = "You don't have that role!"
                                await client.send_message(message.channel, msg)
                                flag = True
            if flag is False:
                msg = 'Something went wrong :shrug:'
                await client.send_message(message.channel, msg)

        if message.content.startswith('!dota random'):
            r = requests.get('https://api.opendota.com/api/heroes/')
            rand = randint(1, len(r.json()))
            msg = """You're going to play {0} a {1} hero with {2} legs""".format(r.json()[rand]["localized_name"],
                                                                                 r.json()[rand]["primary_attr"],
                                                                                 r.json()[rand]["legs"])
            await client.send_message(message.channel, msg)

        if message.content.startswith('!git'):
            msg = """Source for this bot can be found at:
            https://github.com/ville-solja/kukkohelper"""
            await client.send_message(message.channel, msg)
    except:
        e = sys.exc_info()[1]
        LOG.write(str(e))


client.run(TOKEN)