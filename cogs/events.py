from functions import utils as ut
from functions import verificationHandler as vh
from discord.ext import commands
import discord, json
from datetime import datetime

with open("../config.json") as f:
    config = json.load(f)
version = config["version"]

class events(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        role = discord.utils.get(channel.guild.roles, name="Muted")
        perms = discord.PermissionOverwrite(send_messages=False)
        await channel.set_permissions(role, overwrite=perms)
        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        global captchaText
        serverData = ut.openFile(self.client.get_guild(payload.guild_id))
        if payload.message_id == serverData["verification"]["verificationID"] and str(payload.emoji)=="✅":
            embed = discord.Embed(
                title="Verification Captcha",
                description=f"Retype the text in the image below with the\ncommand: ``.verify <text in the image>``\nin {self.client.get_guild(payload.guild_id)} to verify your identity.\n\nExecute ``.verify reload`` to reload captcha.\n\n**Note:** The text is case sensitive",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green()
            )
            captchaText = vh.generateCaptcha()
            vh.bindVerification(user=payload.member, code=captchaText, guild=self.client.get_guild(payload.guild_id))
            file = discord.File("captcha.png", filename="captcha.png")
            embed.set_footer(text=version)
            embed.set_image(url="attachment://captcha.png")
            await payload.member.send(file=file, embed=embed)
        else:
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title='Command error',
                description=f'No matching command detected.',
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Command error",
                description="Missing argument in command.",
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            return
        else:
            raise error

def setup(client):
    client.add_cog(events(client))