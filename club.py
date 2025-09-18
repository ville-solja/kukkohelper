import discord
from setup_logger import logger
from discord.ext import commands
from discord.commands import SlashCommandGroup
import re

class club_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def name_check(self, name: str):
        name = name.lower()
        if name.startswith(self.bot.conf["club_prefix"]):
            return name
        else:
            name = "club-" + name
            return name

    club = SlashCommandGroup("club", "General bot commands for general use")

############################################## BOT EVENTS ##################################################
    ## Helper to set game club channel privileges
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logger.info("Detected new channel created: " + channel.name)
        if(bool(re.match(self.bot.conf["club_prefix"], channel.name))):
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
    @club.command(name="join", description = "Join a club/group. Name is case sensitive probably.")
    async def join(self, ctx, club):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command join called")
        member = ctx.author

        group = self.name_check(club)

        role = discord.utils.get(ctx.guild.roles, name = group)
        if (role == None):
            await ctx.respond("Club not found. Please note that name is case sensitive.")
            logger.info("Group " + group + " not found on server.")
            #await ctx.message.add_reaction(self.bot.conf["emoji_nok"])
        else:
            await member.add_roles(role)
            logger.info("Added " + str(ctx.author) + " to group " + str(role))
            #await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
            await ctx.respond("I added you to group " + str(role))

    @club.command(name="quit", description = "Leave a group/club.")
    async def quit(self, ctx, club):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command quit called")
        member = ctx.author
        group = self.name_check(club)

        role = discord.utils.get(ctx.guild.roles, name = group)
        if(role in member.roles):
            await member.remove_roles(role)
            logger.info("Deleted role " + str(role) + " from " + str(member))
            #await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
            await ctx.respond("I removed you from " + str(role))
        else:
            logger.info("Role " + str(role) + " not found for user " + str(member))
            await ctx.respond("Could not find you in " + group)
            #await ctx.message.add_reaction(self.bot.conf["emoji_nok"])

    @club.command(name="list", description = "List all available clubs.")
    async def list(self, ctx):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command list called")
        roles = ctx.guild.roles
        message = "Here is a list of all the active clubs:\n"
        message = message + "```\n"
        logger.info("Clubs prefix is: " + self.bot.conf["club_prefix"])
        for role in roles:
            logger.info(role.name)
            if(bool(re.match(self.bot.conf["club_prefix"], role.name,  re.IGNORECASE))):
                message = message + role.name + "\n"
        message = message + "```"
        logger.info("Printing following list to user:")
        logger.info(message)
        await ctx.respond(message)

    @club.command(name="create", description = "Create new club/group.")
    async def create_club(self, ctx, club):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command create club called")
        
        group = self.name_check(club)
        role = discord.utils.get(ctx.guild.roles, name = group)
        if (role == None):
            guild = ctx.guild
            await guild.create_role(name=group, mentionable = True)
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
            category = discord.utils.get(ctx.guild.categories, name = self.bot.conf["clubs_category"])
            await guild.create_text_channel(group, overwrites = overwrites, category = category)
            #await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
            await ctx.respond("Club " + group + " created for you! Use /club list and /club join to join now.")
        else:
            await ctx.respond("Club exist already dumkopf.")
            #await ctx.message.add_reaction(self.bot.conf["emoji_nok"])


    @club.command(name="delete", description = "Use carefully.")
    @commands.is_owner()
    async def delete_club(self, ctx, club):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command delete club called")
        group = self.name_check(club)

        channel = discord.utils.get(ctx.guild.channels, name = group)
        role = discord.utils.get(ctx.guild.roles, name = group)

        if (channel != None):
            logger.info("delete channel " + channel.name)
            await channel.delete()
        if (role != None):
            logger.info("delete role " + role.name)
            await role.delete()
        #await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        await ctx.respond("All done.")

    #error handling
    @delete_club.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Only the server owner can delete clubs permanently.")


    @club.command(name="archive", description = "Moves the club to archive category.")
    async def archive_club(self, ctx, club):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command archive club called")
        group = self.name_check(club)

        channel = discord.utils.get(ctx.guild.channels, name = group)
        category = discord.utils.get(ctx.guild.categories, name = self.bot.conf["archive_category"])

        if (channel != None):
            logger.info("archive channel " + channel.name)
            await channel.edit(category=category)
        #await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        await ctx.respond(channel.name + " has been archived")



    @club.command(name="respawn", description = "Respawn the archived club.")
    async def respawn_club(self, ctx, club):
        self.bot.commands_called = self.bot.commands_called + 1
        logger.info("command respawn club called")
        group = self.name_check(club)

        channel = discord.utils.get(ctx.guild.channels, name = group)
        category = discord.utils.get(ctx.guild.categories, name = self.bot.conf["clubs_category"])

        if (channel != None):
            logger.info("respawn channel " + channel.name)
            await channel.edit(category=category)
        #await ctx.message.add_reaction(self.bot.conf["emoji_ok"])
        await ctx.respond(channel.name + " has been returned to active status.")


def setup(bot):
    bot.add_cog(club_helper(bot))