import discord
import requests
import sys
import datetime
from random import randint
from RepeatedTimer import RepeatedTimer

TOKEN = open('TOKEN', 'r').read().strip()
KEY = open('KEY', 'r').read().strip()

emoji_checkmark = '✅'
emoji_stop = '🛑'
emoji_thumbup = '👍'
emoji_thumbdown = '👎'

azure_url_ext = "https://northeurope.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=adult"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": KEY
}
client = discord.Client()
global streamers
streamers = {}
global list_of_invites
list_of_invites = {}


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
    for server in client.servers:
        print(server.name)
        invites = await client.invites_from(server)
        for invite in invites:
            list_of_invites.update({invite.id: {"uses": invite.uses}})


@client.event
async def on_member_update(before, after):
    try:
        after.game.type
    except AttributeError:
        print("member update event ignored")
    else:
        if after.game.type is 1:
            for role in after.roles:
                if role.name == 'Role-Streamer':
                    print('{} passed to user_recently_announced'.format(after))
                    if user_recently_announced(after.name) is False:
                        public_msg = '{0} presents: "{1}"! <{2}>'.format(after, after.game.name, after.game.url)
                        general = discord.utils.get(after.server.channels, name='general')
                        await client.send_message(general, public_msg)
                        invite = await client.create_invite(after.server, max_age = 10800, temporary = True)
                        private_msg = """Here is a link that can be shared with stream audience: {}""".format(invite)
                        await client.send_message(after, private_msg)


@client.event
async def on_member_join(member):
    current = await client.invites_from(member.server)
    for invite_1 in current:
        for invite_2_code, invite_2_uses in list_of_invites.items():
            if invite_1.code == invite_2_code:
                print("code match")
                if invite_1.uses != invite_2_uses["uses"]:
                    print("uses counter difference")
                    print(invite_1.inviter)
                    if 'Helper' in str(invite_1.inviter):
                        print("Helper detected")
                        watcher_role = discord.utils.get(member.server.roles, name='Role-Watcher')
                        await client.add_roles(member, watcher_role)
        list_of_invites.update({invite_1.code: {"uses": invite_1.uses}})
    print(list_of_invites)


@client.event
async def on_message(message):
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
        await client.send_message(message.author, msg)

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
        await client.send_message(message.author, l)

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
        await client.send_message(message.author, msg)

RepeatedTimer(10800, prune_list, streamers) #  occurs every 3 hours

client.run(TOKEN)
