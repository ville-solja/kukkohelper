import discord

file = open('token.txt', 'r')
TOKEN = file.read()

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        msg = """This bot can be used to add yourself to various roles based on games. 
        In order to get full list of games use !list and then get added with !add-<rolename> 
        For example !add-dota will add you to game-dota role and rights that come with it"""
        await client.send_message(message.channel, msg)

    if message.content.startswith('!list'):
        l = 'Here is a list of game roles in this channel\n'
        for s in client.servers:
            for r in s.roles:
                if r.name.startswith('Game-'):
                    l += '{0}\n'.format(r)
        await client.send_message(message.channel, l)

    if message.content.startswith('!add'):
        flag = False
        for s in client.servers:
            for r in s.roles:
                if r.name.startswith('Game-'):
                    if str(r.name).lower() == str(message.content[5:]).lower():
                        await client.add_roles(message.author, r)
                        msg = 'Added role {0} for user {1}'.format(r, message.author)
                        await client.send_message(message.channel, msg)
                        flag = True
        if flag == False:
            msg = 'Role not found or something else went wrong :shrug:'
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for each in client.servers:
       print(each.name)

client.run(TOKEN)