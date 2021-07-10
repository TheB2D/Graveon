import json
import os

def initialize(serverName, dateInitialized, initializeAuthor):
    serverData={
        "serverName": f"{serverName}",
        "dateInitialized": f"{dateInitialized}",
        "initializeAuthor": f"{initializeAuthor}",
        "inviteLink": None,
        "bannedWords": [],
        "settings": {
            "familyMode": False,
            "banAppeal": {
                "allowAppeal": False,
                "appealChannel": None
            },
            "logMessages": False,
            "logReactions": False,
            "logGuild": False,
        },
        "RolePermissions": {
            "warnRoles": [],
            "banRoles": [],
            "kickRoles": []
        },
        "serverWarns": {
        },
        "verification": {
            "verificationChannelID":None,
            "verificationID":None,
            "verificationRole":None
        },
        "verifiedUsers":[]
    }
    logFile = (str(serverName)).replace(" ", "")
    open(f"../serverLogs/{logFile}.log", mode='a').close()
    with open(f'../serverFiles/{serverName}.json', 'w') as f:
        json.dump(serverData, f, indent=2)


def isInitialized(server):
    if f"{server}.json" in os.listdir("../serverFiles"):
        return True
    elif f"{server}.json" not in os.listdir("../serverFiles"):
        return False

async def is_initialized(ctx):
    return isInitialized(ctx.guild)==True

def openFile(guild):
    with open(f"../serverFiles/{guild}.json") as f:
        serverData = json.load(f)
        return serverData