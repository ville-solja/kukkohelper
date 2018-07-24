import discord
import requests
from random import randint

file = open('/opt/scripts/kukkohelper/token.txt', 'r')
TOKEN = file.read()

client = discord.Client()

client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!help'):
        msg = """This bot will help you find people to play games with!
        Commands: 
        "!list" shows all available games
        "!add <game>" adds you to chosen game role
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
        for server in client.servers:
            for role in server.roles:
                if role.name.startswith('Game-'):
                    if str(role.name[5:]).lower() == str(message.content[5:]).lower():
                        await client.add_roles(message.author, role)
                        msg = 'Added role {0} for user {1}'.format(role, message.author)
                        await client.send_message(message.channel, msg)
                        flag = True
        if flag == False:
            msg = 'Role not found or something else went wrong :shrug:'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!dota random'):
        r = requests.get('https://api.opendota.com/api/heroes/')
        rand = randint(0,len(r.json()-1))
        msg = """You're going to play {0} a {1} hero with {2} legs""".format(r.json()[rand]["localized_name"],r.json()[rand]["primary_attr"],r.json()[rand]["legs"])
        await client.send_message(message.channel, msg)

    if message.content.startswith('!git'):
        msg = """Source for this bot can be found at:
        https://github.com/ville-solja/kukkohelper"""
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for each in client.servers:
       print(each.name)

client.run(TOKEN)
