import discord, json, os
from functions import utils as ut
from discord.ext import commands
from datetime import datetime


# ==========================================================
# ░██████╗░██████╗░░█████╗░██╗░░░██╗███████╗░█████╗░███╗░░██╗
# ██╔════╝░██╔══██╗██╔══██╗██║░░░██║██╔════╝██╔══██╗████╗░██║
# ██║░░██╗░██████╔╝███████║╚██╗░██╔╝█████╗░░██║░░██║██╔██╗██║
# ██║░░╚██╗██╔══██╗██╔══██║░╚████╔╝░██╔══╝░░██║░░██║██║╚████║
# ╚██████╔╝██║░░██║██║░░██║░░╚██╔╝░░███████╗╚█████╔╝██║░╚███║
# ░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚══╝
# ===============Developed by B2D#9992=======================
#                     .CHR.T.KHNG.

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix = '.', intents=intents)

with open("../config.json") as f:
    config = json.load(f)

version = config["version"]

cogs = ["verification", "events"]
if __name__=='__main__':
    print(f"Discord bot running on {version}")
    for cog in cogs:
        client.load_extension(f"cogs.{cog}")

client.load_extension("cogs.moderation")

@client.command()
@commands.has_permissions(administrator=True)
@commands.guild_only()
async def initialize(ctx, type=None):
    global serverData
    if type=="re":
        initializeMsg = discord.Embed(
            title="Initialize Setup",
            description=f"{ctx.guild} has been\nsuccessfully re-initialized. A DM\nhas been sent to you for more\ninformation.\n``Note: Config has been reseted``",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        initializeMsg.set_footer(text=version)
        ut.initialize(
            serverName=ctx.guild,
            dateInitialized=datetime.utcnow(),
            initializeAuthor=ctx.author
        )
        await ctx.message.add_reaction('✅')
        await ctx.send(embed=initializeMsg)
        initializeDm = discord.Embed(
            title="Initialize Setup",
            description=f"""
            **Server name**: {ctx.guild}
            **Date initialized**: {datetime.utcnow()}
            **Initialization by**: {ctx.author}
            
            Initializing your server enables you to unlock
            more features that requires a database, such
            as logging, verifications, configs, etc.
            """
        )
        await ctx.author.send(embed=initializeDm)
    elif f"{ctx.guild}.json" in os.listdir("../serverFiles"):
        await ctx.message.add_reaction('❌')
        initializeMsg = discord.Embed(
            title="Initialize Setup",
            description=f"{ctx.guild} has already\nbeen initialized!",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        initializeMsg.set_footer(text=version)
        await ctx.send(embed=initializeMsg)

    else:
        initializeMsg= discord.Embed(
            title="Initialize Setup",
            description=f"{ctx.guild} has been\nsuccessfully initialized. A DM\nhas been sent to you for more\ninformation.",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        initializeMsg.set_footer(text=version)
        ut.initialize(
            serverName=ctx.guild,
            dateInitialized=datetime.utcnow(),
            initializeAuthor=ctx.author
        )
        await ctx.message.add_reaction('✅')
        await ctx.send(embed=initializeMsg)
        initializeDm = discord.Embed(
            title="Initialize Setup",
            description=f"""
            **Server name**: {ctx.guild}
            **Date initialized**: {datetime.utcnow()}
            **Initialization by**: {ctx.author}

            Initializing your server enables you to unlock
            more features that requires a database, such
            as logging, verifications, configs, etc.
            """
        )
        await ctx.author.send(embed=initializeDm)


@client.command()
async def quit(ctx):
    embed = discord.Embed(
        title='Graveon',
        description=f'Graveon bot is shutting down.\nAccess the console to start it up!',
        colour=discord.Colour.dark_grey(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text=version)
    await ctx.send(embed=embed)
    return await client.close()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('.help'))
    print(f'Graveon is ready! Logged in as {client.user.name} - {client.user.id}')

@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title = 'Graveon',
        description = f'Current bot lantecy: {round(client.latency * 1000)}ms',
        colour = discord.Colour.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text='Thank you using Graveon bot!')
    await ctx.send(embed=embed)

client.run(config["token"])
