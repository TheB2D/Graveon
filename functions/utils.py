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
            "ifReaches": {
                "warn3": "Mute1hr",
                "warn5": "Mute24hr"
            },
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
    open(f"../serverLogs/{serverName}.log", mode='a').close()
    with open(f'../serverFiles/{serverName}.json', 'w') as f:
        json.dump(serverData, f, indent=2)


def isInitialized(server):
    if f"{server}.json" in os.listdir("../serverFiles"):
        return True
    elif f"{server}.json" not in os.listdir("../serverFiles"):
        return False

def openFile(guild):
    with open(f"../serverFiles/{guild}.json") as f:
        serverData = json.load(f)
        return serverData