import discord
import requests
import sys
import os
from datetime import datetime
from random import randint
import matplotlib.pyplot as plt
import io
import re
from wordcloud import WordCloud

TOKEN = os.environ['TOKEN']    
#TOKEN = '<Insert token for local testing>'
KEY = os.environ.get('KEY')
#KEY = None 
if KEY is not None:
    KEY = os.environ['KEY']
    AzureFilterEnabled = True
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": KEY
    }
    azure_url_ext = "https://northeurope.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=adult"
else: 
    AzureFilterEnabled = False

emoji_checkmark = '✅'
client = discord.Client()
wordlist = []
link_pattern = re.compile('^http')
emoji_pattern = re.compile('^:.*:$')
cmd_pattern = re.compile('^!')

@client.event
async def on_ready():
    print('{} bot started'.format(
        datetime.now().strftime("%d.%m.%Y, %H:%M:%S")))
    print('Client Name: {}'.format(
        client.user.name))
    print('Client ID: {}'.format(
        client.user.id))
    for guild in client.guilds:
        print('Guild: {}'.format(
            guild.name))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if AzureFilterEnabled == True:
        if len(message.attachments) > 0:
            data = {'url': '{0}'.format(message.attachments[0].url)}
            r = requests.post(azure_url_ext, json=data, headers=headers)
            if r.json()['adult']['isAdultContent'] is True:
                if message.channel.is_nsfw() is False:
                    await message.delete()
                    msg = 'Image was deleted due to Adultscore: {0}.\nPlease repost to NSFW'.format(
                        r.json()['adult']['adultScore'])
                    print('{} Image deleted due to NSFW score of {} from {}'.format(
                        datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
                        r.json()['adult']['adultScore'], 
                        message.channel.name))
                    await message.channel.send(msg)
            else:
                await message.add_reaction(emoji_checkmark)      

    if message.content.startswith('!help'):
        msg = """This bot will help you find people to play games with!
        Commands:
        "!help" displays this message
        "!list" shows all available roles that can be used with add/remove
        "!add <role>" adds you to chosen role. Example: !add dota
        "!remove <role>" removes role if you have it. Example !remove dota
        "!dota random" picks a random dota hero from Opendota API
        "!wordcloud" creates a wordcloud from that channels message history
        """
        print('{} help requested by {}'.format(
            datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
            message.author))
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
        print('{} role list requested by {}'.format(
            datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
            message.author))
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
                                print('{} role addded requested by {}'.format(
                                    datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
                                    message.author))
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
                                print('{} role removed requested by {}'.format(
                                    datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
                                    message.author))
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
        print('{} random dota hero requested by {}'.format(
            datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
            message.author))
        await message.channel.send(msg)

    if message.content.startswith('!wordcloud'):
        print('{} wordcloud requested by {}'.format(
            datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
            message.author))
        async for message in message.channel.history(limit=None):
            if re.match(cmd_pattern, message.content) is not None:
                print('this is a command')
            else:
                message_as_list = message.content.split()
                print(message_as_list)
                for word in message_as_list:
                    if len(word) < 4:
                        print('this is too short')
                    elif re.match(link_pattern, word) is not None:
                        print('this is a link')
                    elif re.match(emoji_pattern, word) is not None:
                        print('this is a emoji')
                    else:
                        wordlist.append(word)    
        wordlist_str = ' '.join(wordlist)
        wordcloud = WordCloud(max_font_size=40, background_color='black').generate(wordlist_str)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        image = io.BytesIO() 
        plt.savefig(image, transparent=True, format='png')
        image.seek(0)
        print('{} wordcloud completed for {}'.format(
            datetime.now().strftime("%d.%m.%Y, %H:%M:%S"), 
            message.author))
        await message.channel.send(content= "Tässä hieno wordcloud", file=discord.File(image, 'image.png'))
client.run(TOKEN)