import json, discord

def modify(guild, section, type, *, args) -> list:
    """

    :param guild:
    :param section:
    :param type:
    :param args:
    :return: list format [string, color of embed]
    """
    global default
    with open(f"../serverFiles/{guild}.json") as f:
        serverConfig = json.load(f)
    response = None
    if section == "banned_words":
        if type == "add":
            if args in serverConfig["bannedWords"]:
                response = [f"❌ {args} is already in the list of banned words", discord.Colour.red()]
            else:
                for arg in args:
                    serverConfig["bannedWords"].append(str(arg))
                response = [f"✅ added \"{', '.join(args)}\" to the list of banned words", discord.Colour.dark_green()]
        elif type == "remove":
            if args not in serverConfig["bannedWords"]:
                response = [f"❌ {args} is not a banned word", discord.Colour.red()]
            else:
                serverConfig["bannedWords"].remove(args)
                response = [f"✅ removed {args} to the list of banned words", discord.Colour.dark_green()]
        elif type == "clear":
            serverConfig["bannedWords"].clear()
            response = ["✅ successfully cleared all banned words", discord.Colour.dark_green()]

    elif section == "family_mode":
        if type == "true":
            if "family-friendly" not in serverConfig["bannedWords"]:
                serverConfig["bannedWords"].append("family-friendly")
                serverConfig["settings"]["familyMode"] = True
                response = [f"✅ Family mode enabled!", discord.Colour.dark_green()]
            elif "family-friendly" in serverConfig["bannedWords"]:
                response = [f"❌️ Family mode is already enabled", discord.Colour.red()]
        elif type == "false":
            if "family-friendly" not in serverConfig["bannedWords"]:
                response = [f"❌️ Family mode was already disabled", discord.Colour.red()]
            elif "family-friendly" in serverConfig["bannedWords"]:
                serverConfig["bannedWords"].remove("family-friendly")
                serverConfig["settings"]["familyMode"] = False
                response = [f"✅ Family mode disabled!", discord.Colour.dark_green()]
        else:
            return [0]

    elif section == "log_messages":
        logMessages = serverConfig["settings"]["logMessages"]
        if type == "true":
            if logMessages != True:
                serverConfig["settings"]["logMessages"] = True
                response = [f"✅ Message logging enabled!", discord.Colour.dark_green()]
            elif logMessages == True:
                response = [f"❌ Message logging was already enabled", discord.Colour.red()]
        elif type == "false":
            if logMessages != False:
                serverConfig["settings"]["logMessages"] = False
                response = [f"✅ Message logging disabled", discord.Colour.dark_green()]
            elif logMessages == False:
                response = [f"❌ Message logging was already disabled", discord.Colour.red()]

    elif section == "log_react":
        if type == "true":
            serverConfig["logReactions"] = True
            pass
        elif type == "false":
            serverConfig["logReactions"] = False
            pass

    elif section == "log_guild":
        if type == "true":
            serverConfig["logGuild"] = True
        elif type == "false":
            serverConfig["logGuild"] = False
            pass

    with open(f'../serverFiles/{guild}.json', 'w') as f:
        json.dump(serverConfig, f, indent=2)
    return response

def link_disable(ctx, type, args: discord.TextChannel):
    with open(f"../serverFiles/{ctx.guild}.json") as f:
        serverConfig = json.load(f)
    if type == "add":
        if args[0].name not in serverConfig["settings"]["disableLinks"]:
            serverConfig["settings"]["disableLinks"].append(str(args[0].name))
            response=[f"✅ links will no longer be sendable in #{args[0]}", discord.Colour.green()]
        else:
            response = ["❌ links in this channel is already disabled", discord.Colour.red()]
    elif type == "remove":
        if args[0].name in serverConfig["settings"]["disableLinks"]:
            serverConfig["settings"]["disableLinks"].remove(str(args[0].name))
            response = [f"✅ links will now be sendable in {args[0]}", discord.Colour.green()]
        else:
            response=["❌ links in this channel is already enabled", discord.Colour.red()]
    else:
        response = ["Uh oh. Something went wrong...", discord.Colour.orange()]
    with open(f"../serverFiles/{ctx.guild}.json", "w") as f:
        json.dump(serverConfig, f, indent=2)
    return response

def currentConfig(guild):
    with open(f"../serverFiles/{guild}.json") as f:
        serverConfig = json.load(f)
    if len(serverConfig['bannedWords'])==0:
        bannedWords="No banned words"
    else:
        bannedWords=', '.join(serverConfig['bannedWords'])
    response=f"""
    🚫`` Banned words: (banned_words)`` {bannedWords}
    👨‍👩‍👦`` Family-friendly mode (family_mode):`` {str(serverConfig['settings']['familyMode'])}
    📝`` Logging:``
    > ↳Messages (log_messages): {serverConfig['settings']['logMessages']}
    > ↳Reaction events (log_react): True
    > ↳Guild modification events (log_guild): True
    🚫``Disable link sending:``  {'No channels' if len(serverConfig['settings']['disableLinks']) == 0 else ", ".join(serverConfig['settings']['disableLinks'])}
    """
    return response
