##from kukkohelper import active
import discord
from setup_logger import logger
from discord.ext import commands
import re

class cock_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
############################################## BOT EVENTS ##################################################
    ## Helper to set game club channel privileges
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logger.info("Detected new channel created: " + channel.name)
        if(bool(re.match("game-", channel.name))):
            role = discord.utils.get(channel.guild.roles, name = channel.name)
            logger.info("Found role " + role.name)
            if(role==None):
                logger.warning("This probably shouldn't happen :E")
            else:
                logger.info("Set default permissions: role " + role.name + " can send messages to channel " + channel.name)
                await channel.set_permissions(role, send_messages=True)
                await channel.set_permissions(role, view_channel=True)
############################################## END BOT EVENTS ##############################################

################################################ BOT COMMANDS ##############################################
    @commands.command(name="ping", help = "Test if bot is online/active", aliases = ["p"])
    async def ping(self, ctx):
        logger.info("command ping called")
        ##if(active()):
        await ctx.send("Pong! Bot functions online")
        ##else:
           ## await ctx.send("Bot functions currently offline.")


    @commands.command(name="join", brief = "Join a group.", help = "Join a gaming group. Group/Role name is case sensitive!!")
    async def join(self, ctx, group):
        logger.info("command join called")
        member = ctx.message.author

        is_game = bool(re.match("game",group,  re.IGNORECASE))

        if(is_game):
            group = group.lower()
            role = discord.utils.get(ctx.guild.roles, name = group)
            if (role == None):
                await ctx.send("Group not found. Please note that group name is case sensitive.")
                logger.info("Group " + group + " not found on server.")
            else:
                await member.add_roles(role)
                logger.info("Added " + str(ctx.message.author) + " to group " + str(role))
                await ctx.send("I added you to group " + str(role))
        else:
            await ctx.send("You can only add groups with Game- prefix currently.")

    @commands.command(name="quit", brief= "Leave a group.", help = "Leave a gaming group. Group/Role name is case sensitive!!")
    async def quit(self, ctx, group):
        logger.info("command quit called")
        member = ctx.message.author
        group = group.lower()

        role = discord.utils.get(ctx.guild.roles, name = group)
        if(role in member.roles):
            await member.remove_roles(role)
            logger.info("Deleted role " + str(role) + " from " + str(member))
            await ctx.send("I removed you from " + str(role))
        else:
            logger.info("Role " + str(role) + " not found for user " + str(member))
            await ctx.send("Could not find you in " + group)

    @commands.command(name="list", brief = "List gaming groups.")
    async def list(self, ctx):
        logger.info("command list called")
        roles = ctx.guild.roles
        logger.info("Printing following list to user:")
        message = "```\n"

        for role in roles:
            if(bool(re.match("game", str(role),  re.IGNORECASE))):
                message = message + str(role) + "\n"
        message = message + "```"
        logger.info(message)
        await ctx.send(message)

    @commands.command(name="create_club", brief = "Create new gaming group", help = "Create new gaming group. Must have game- prefix.", aliases=['create', 'cc'])
    async def create_club(self, ctx, group):
        logger.info("command create club called")
        
        group = group.lower()
        if(bool(re.match("game-", group))):
            role = discord.utils.get(ctx.guild.roles, name = group)
            if (role == None):
                guild = ctx.guild
                await guild.create_role(name=group)
                overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
                category = discord.utils.get(ctx.guild.categories, name = "CLUBS")
                await guild.create_text_channel(group, overwrites = overwrites, category = category)
                await ctx.send("Gayming group " + group + " created for you! Use !list and !join to join now.")
            else:
                await ctx.send("Group exist already dumkopf.")
        else:
            await ctx.send("Group name must have game- prefix. Try again nakkisormi.")  

    @commands.command(name="delete_club", aliases=["del_club", "dc"], brief = "Delete existing gaming group.", help = "Use carefully.")
    async def delete_club(self, ctx, group):
        logger.info("command delete club called")
        group = group.lower()

        if(bool(re.match("game-", group))):
            channel = discord.utils.get(ctx.guild.channels, name = group)
            role = discord.utils.get(ctx.guild.roles, name = group)

            if (channel != None):
                logger.info("delete channel " + channel.name)
                await channel.delete()
            if (role != None):
                logger.info("delete role " + role.name)
                await role.delete()
            await ctx.send("All done.")
        else:
            await ctx.send("Don't try any funny business! Only gaming clubs can be deleted.")

def setup(bot):
    bot.add_cog(cock_helper(bot))