from functions import utils as ut, verificationHandler as vh, moderationHandler as mod, logger
from discord.ext import commands
import discord, json
from datetime import datetime

with open("../config.json") as f:
    config = json.load(f)
version = config["version"]

class events(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        ctx = await self.client.get_context(message) # context
        if message.author == self.client.user:
            return
        elif ctx.valid:  # auto mod that detects banned messages do not include message that invoke commands
            logger.log(message, "execute") #logs event
            return
        else:
            logger.log(message, "message") #logs message
        await self.client.process_commands(message)
        if ut.isInitialized(message.guild) == True:
            serverData = ut.openFile(message.guild)
            if "family-friendly" in serverData["bannedWords"]:
                with open("../serverFiles/defaultBadWords.json") as f:
                    badWordsFile = json.load(f)
                for badWord in badWordsFile:
                    serverData["bannedWords"].append(badWord)
            for word in serverData["bannedWords"]:
                if word in message.content.lower():
                    mod.warn(member=message.author, server=message.guild)
                    if serverData["serverWarns"][str(message.author)] != True: # checks if author key exists, if not then it has no warns
                        currentWarns = 0
                    else:
                        currentWarns = serverData["serverWarns"][str(message.author)]
                    embed = discord.Embed( #TODO: invoke instead of writing the embed again
                        title="Warn Notice",
                        description=f"**{message.author}** has been warned!\n**Reason:** Saying a banned word\n**Current Warns:** {currentWarns + 1}",
                        colour=discord.Colour.orange(),
                        timestamp=datetime.utcnow()
                    )
                    embed.set_footer(text=version)
                    await message.delete()
                    await message.channel.send(embed=embed)
                    embedDM = discord.Embed(
                        title="Warn Notice",
                        description=f"You have been warned in **{message.guild}**\n**Reason:** Saying a banned word\n**Current Warns:** {currentWarns + 1}",
                        colour=discord.Colour.orange(),
                        timestamp=datetime.utcnow()
                    )
                    embedDM.set_footer(text=version)
                    await message.author.send(embed=embedDM)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """ sync permissions when a new channel is created """
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
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Command error",
                description="The guild that you're in must be\ninitialized to be able to execute this command",
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