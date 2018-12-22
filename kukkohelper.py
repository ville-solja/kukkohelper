import discord
import requests
import platform
import sys
import random
from random import randint

platform = platform.system()
if platform == 'Windows':
    file = open('token.txt', 'r')
    key = open('key.txt', 'r')
    log = open('discord_error_kukko.log', 'w')
elif platform == 'Linux':
    file = open('/opt/scripts/kukkohelper/token.txt', 'r')
    key = open('/opt/scripts/kukkohelper/key.txt', 'r')
    log = open('/tmp/discord_error_kukko.log', 'w')

TOKEN = file.read().strip()
KEY = key.read().strip()

emoji_checkmark = '✅'
emoji_stop = '🛑'
emoji_thumbup = '👍'
emoji_thumbdown = '👎'
emoji_winter = '🎅'

azure_url_ext = "https://northeurope.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=categories,tags,description,adult"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": "cd4fef3d2fc247fda41283e1988f366e"
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
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if len(message.attachments) > 0:
            data = {'url': '{0}'.format(message.attachments[0]['url'])}
            r = requests.post(azure_url_ext, json=data, headers=headers)
            channel = discord.utils.get(message.server.channels, name='nsfw')
            content = message.attachments[0]['url']
            if r.json()['adult']['isAdultContent'] is True:
                print('Adult content detected')
                await client.delete_message(message)
                msg = 'Message deleted from {0}. Image can be accessed from this link {1}'.format(message.channel, content)
                print(msg)
                await client.send_message(channel, msg)
            else:
                await client.add_reaction(message, emoji_thumbup)

        if message.content.startswith('!help'):
            msg = """This bot will help you find people to play games with!
            Commands: 
            "!list" shows all available games
            "!add <game>" adds you to chosen game role
            "!dota random" picks a random dota hero
            "!git" posts a link to the bots source
            """
            await client.send_message(message.channel, msg)

        if message.content.startswith('!list'):
            l = 'Here is a list of game roles in this channel\n'
            for s in client.servers:
                for r in s.roles:
                    if r.name.startswith('Game-'):
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
            if flag == False:
                msg = 'Role not found or something else went wrong :shrug:'
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
        log.write(str(e))


client.run(TOKEN)

