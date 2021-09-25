from functions import utils
from functions import configurationHandler as config
from discord.ext import commands
import discord, asyncio, os, typing

class configurations(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['c'], name="config", description="**Customize Graveon in your server with this command**", usage="[section: server, log, disable_links, family_mode, log_messages, log_react, log_guild, banned_words] [OPTIONAL (actions): add, remove, clear, dump, true, false]")
    async def config(self, ctx, section, type=None, *arg: typing.Union[discord.TextChannel, str]):
        if section=="server":
            embed = discord.Embed(
                title="⚙️ Server Configurations",
                description=f"**To modify a certain setting use the commmand:**\n``.config <section> <modification> <modification parameter>``\n**To learn more about a config section use the command:**\n``.config help <section>``\n{config.currentConfig(ctx.guild)}",
                colour=discord.Colour.blurple()
            )
            await ctx.send(embed=embed)
        elif section=="log":
            if type=="dump":
                f = open(f"../serverLogs/{ctx.guild}.log", "r")
                lines = f.readlines()
                send = "".join(lines)
                try:
                    embed = discord.Embed(
                        title=f"Here you go!",
                        description=send,
                        color=discord.Colour.blurple()
                    )
                    embed.set_footer(text="Log files eventually will be full, to empty them execute: \".config log clear\"")
                    await ctx.send(embed=embed)
                except discord.errors.HTTPException:
                    await ctx.send("Log file is too big!!!")
                    # TODO: selector
                    pass
                f.close()
            elif type=="clear":
                f = open(f"../serverLogs/{ctx.guild}.log", "w")
                f.write("")
                f.close()
                embed = discord.Embed(
                    title=f"✅ Successfully cleared the log file!",
                    color=discord.Colour.green()
                )
                await ctx.send(embed=embed)
        elif section == "disable_links":
            modify = config.link_disable(ctx=ctx, type=type, args=arg)
            embed = discord.Embed(
                title=modify[0],
                color=modify[1]
            )
            await ctx.send(embed=embed)
        elif section!="server":
            try:
                modify = config.modify(guild=ctx.guild, section=section, type=type, args=arg)
                embed = discord.Embed(
                    title=modify[0],
                    color=modify[1]
                )
            except:
                embed = discord.Embed(
                    title="An error occurred!",
                    description=f"Error hint: {section} may not be a section in config. settings!",
                    color=discord.Colour.red()
                )
            await ctx.send(embed=embed)
            return

        return

def setup(client):
    client.add_cog(configurations(client))
