from functions import moderationHandler as fn
from functions import utils
from discord.ext import commands
import discord, json
from datetime import datetime

with open("../config.json") as f:
    config = json.load(f)
version = config["version"]


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='kick', description='**Kick people out of the guild', usage='[member] [OPTIONAL: reason]')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embedDM = discord.Embed(
            title='Kick Notice',
            description=f'{ctx.author.name} kicked you in {ctx.guild}!\n**Reason:** {reason}'
        )
        embedDM.set_footer(text=version)
        await member.send(embed=embedDM)
        await member.kick(reason=reason)
        embed = discord.Embed(
            title='Kick Notice',
            description=f'{member} has been kicked\n **Reason**: {reason}',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=version)
        await ctx.send(embed=embed)

    @commands.command(name='ban', description='**Ban people in the guild**', usage='[member] [OPTIONAL: reason]')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title='Ban Notice',
            description=f'You have been banned by {ctx.author.name}\nin {ctx.guild}\n **Reason**: {reason}',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=version)
        await member.send(embed=embed)
        await member.ban(reason=reason)
        embed = discord.Embed(
            title='Ban Notice',
            description=f'{member} has been banned!\n **Reason**: {reason}',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=version)
        await ctx.send(embed=embed)

    @commands.command(name='unban', description='**Unban people out of the guild**', usage='[member]')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def unban(self, ctx, *, member):
        """ inefficient unban command, will change next commit"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
        embed = discord.Embed(
            title='Unban Notice',
            description=f'{member} has been unbanned!',
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=version)
        await ctx.send(embed=embed)

    @commands.command(name='mute', description='**Remove a member\'s permission to speak**', usage='[member]')
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member):
        if discord.utils.get(ctx.guild.roles, name='Muted') not in ctx.guild.roles:
            await ctx.guild.create_role(name='Muted')
        perms = discord.PermissionOverwrite(send_messages=False)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, overwrite=perms)
        await member.add_roles(role)
        embed = discord.Embed(
            title="Mute Notice",
            description=f"{ctx.author} has muted **{member}**",
            colour=discord.Colour.orange(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
        embedDM = discord.Embed(
            title="Mute Notice",
            description=f"{ctx.author} muted you in **{ctx.guild}!**",
            colour=discord.Colour.orange(),
            timestamp=datetime.utcnow()
        )
        embedDM.set_footer(text=version)
        await member.send(embed=embedDM)

    @commands.command(name='unmute', description='**Return a member\'s permission to speak**', usage='[mumber]')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(embed=discord.Embed(title="Mute Notice", description=f"{member} has been unmuted by {ctx.author}", timestap=datetime.utcnow(), colour=discord.Colour.orange()).set_footer(text=version))

    @commands.check(utils.is_initialized)
    @commands.command(name='warn', description='Warn a member', usage='[member] [OPTIONAL: reason]')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if utils.isInitialized(ctx.guild) == True:
            serverData = utils.openFile(ctx.guild)  # sever properties
            fn.warn(member=member, server=ctx.guild)  # warns the user
            embed = discord.Embed(
                title="Warn Notice",
                description=f"{ctx.author} has warned **{member}**\n**Reason:** {reason}",
                colour=discord.Colour.orange(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=version)
            await ctx.send(embed=embed)  # send warning embed to channel
            currentWarns = serverData["serverWarns"][f"{ctx.author}"]+1  # grabs ctx.author current warns from json
            embedDM = discord.Embed(
                title="Warn Notice",
                description=f"You have been warned in **{ctx.guild}**\n**Reason:** {reason}\n**Current Warns:** {currentWarns}",
                colour=discord.Colour.orange(),
                timestamp=datetime.utcnow()
            )
            embedDM.set_footer(text=version)
            await member.send(embed=embedDM)  # sends warning to dm
        elif utils.isInitialized(ctx.guild) == False:
            embed = discord.Embed(
                title="Initialization",
                description=f"Initialize {ctx.guild} first before\nexecuting moderation commands!",
                colour=discord.Colour.orange(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="do \".initialize\" to initialize")
            await ctx.send(embed=embed)

    @commands.command(name='clear', description='**This command will clear messages**', usage='[amount of messages]')
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=discord.Embed(title=f"✅ Successfully cleared {amount} messages!", color=discord.Colour.green()))

    @kick.error
    @ban.error
    @unban.error
    async def test_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='Graveon',
                description="You're missing the required permissions to execute this command",
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text='Gain access to all commands by being Administrator')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(moderation(client))