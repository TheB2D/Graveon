from functions import verificationHandler as handler
from functions import utils as ut
from discord.ext import commands
import discord, json
from datetime import datetime

with open("../config.json") as f:
    config = json.load(f)
version = config["version"]

class verification(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.check(ut.is_initialized)
    @commands.command()
    async def verification(self, ctx, type, role : discord.Role=None):
        serverData = ut.openFile(ctx.guild)
        if type == "set" or type=="re" and ctx.message.channel.id != serverData["verification"]["verificationChannelID"]:
            await ctx.message.delete()
            embed = discord.Embed(
                title="Verification captcha",
                description="React to the ✅ emoji bellow to receive\na verification captcha in your dms!\n\n**How to verify:**\nYou'll receive a dm with a captcha after\nreacting to this message retype the\ncaptcha here with: ``.verify <code>``",
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=version)
            message = await ctx.send(embed=embed)
            messageFetched = await ctx.channel.fetch_message(message.id)
            await messageFetched.add_reaction('✅')
            handler.setVerificationChannel(id=message.id, channelID=messageFetched.channel.id, guild=ctx.guild)
        elif type == "set" and ctx.message.channel.id == serverData["verification"]["verificationChannelID"]:
            embed = discord.Embed(
                title="Verification Set",
                description="There is already a verification captcha\nin this channel!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.orange()
            )
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
        elif type == "role":
            handler.setVerificationRole(role=role, guild=ctx.guild)
            embed = discord.Embed(
                title="Verification Role Set",
                description=f"Verification role is now {role.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green()
            )
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
        elif type is None:
            embed = discord.Embed(
                title="Verification Error",
                description="Verification command not recognized!",
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=version)
            await ctx.send(embed=embed)

    @commands.command()
    async def verify(self, ctx, code=None):
        await ctx.message.delete()
        with open(f"../functions/temporary/verificationBinds.json") as f:
            binds = json.load(f)
        if code == "reload":
            embed = discord.Embed(
                title="Verification Captcha",
                description=f"Retype the text in the image below with the\ncommand: ``.verify <text in the image>``\nin {ctx.guild} to verify your identity.\n\nExecute ``.verify reload`` to reload captcha.\n\n**Note:** The text is case sensitive",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green()
            )
            captchaText = handler.generateCaptcha()
            handler.bindVerification(user=ctx.author, code=captchaText, guild=ctx.guild)
            file = discord.File("captcha.png", filename="captcha.png")
            embed.set_footer(text=version)
            embed.set_image(url="attachment://captcha.png")
            await ctx.author.send(file=file, embed=embed)
            return
        elif binds["verificationBinds"][f"{ctx.author}"][0] == code:
            await ctx.author.send(f'✅ You are now verified in {binds["verificationBinds"][f"{ctx.author}"][1]}!')
            role = discord.utils.get(ctx.guild.roles, name=f"{handler.retrieveVerifiedRole(ctx.guild)}")
            await ctx.author.add_roles(role)
            del binds["verificationBinds"][f"{ctx.author}"] # TODO: this doesnt work for some reason
        elif binds["verificationBinds"][f"{ctx.author}"][0]!= code:
            await ctx.author.send("❌ **Verification failed**: Incorrect code! Try again.")
        else:
            await ctx.author.send("❌ **Verification error**: You don't have a CAPTCHA to solve!.")
        with open(f"../functions/temporary/verificationBinds.json", "w") as f:
                json.dump(binds, f, indent=2)


def setup(client):
    client.add_cog(verification(client))