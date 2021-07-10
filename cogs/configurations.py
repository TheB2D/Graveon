from functions import utils
from functions import configurationHandler as config
from discord.ext import commands
import discord, asyncio, os

class configurations(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['config'])
    @commands.has_permissions(administrator=True)
    async def configuration(self, ctx, section, type=None, *arg):
        """
            :param ctx: context
            :param type: (section of settings) banned_words
            :param type2: (true or false, add or remove)
            :param arg: pass on to type 2 (what to add)
            :return: none
        """
        if section=="server":
            embed = discord.Embed(
                title="⚙️ Server Configurations",
                description=f"**To modify a certain setting use the commmand:**\n``.config <section> <modification> <modification parameter>``\n**To learn more about a config section use the command:**\n``.config help <section>``\n{config.currentConfig(ctx.guild)}",
                colour=discord.Colour.blurple()
            )
            await ctx.send(embed=embed)
        if section!="server":
            modify = config.modify(guild=ctx.guild, section=section, type=type, args=arg)
            embed = discord.Embed(
                title=modify[0],
                color=modify[1]
            )
            await ctx.send(embed=embed)
        if section=="log" and type=="dump":
            f = open(f"../serverLogs/{ctx.guild}.log", "r")
            lines = f.readlines()
            send = "".join(lines)
            embed = discord.Embed(
                title="Here you go!",
                description=send,
                color=discord.Colour.blurple()
            )
            f.close()
            await ctx.send(embed=embed)
        return

def setup(client):
    client.add_cog(configurations(client))
