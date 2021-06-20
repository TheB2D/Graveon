import json
import random
import string
from captcha.image import ImageCaptcha

def setVerificationChannel(id, channelID, guild) -> None:
    with open(f"../serverFiles/{guild}.json") as f:
        serverData = json.load(f)
    serverData["verification"]["verificationChannelID"] = channelID
    serverData["verification"]["verificationID"] = id
    with open(f'../serverFiles/{guild}.json', 'w') as f:
        json.dump(serverData, f, indent=2)
    return

def bindVerification(user, code, guild) -> bool:
    with open(f"../functions/temporary/verificationBinds.json") as f:
        serverData = json.load(f)
    serverData["verificationBinds"][f"{user}"]=[code, str(guild)]
    with open(f"../functions/temporary/verificationBinds.json", 'w') as f:
        json.dump(serverData, f, indent=2)
    return True

def setVerificationRole(role, guild) -> bool:
    with open(f"../serverFiles/{guild}.json") as f:
        serverData = json.load(f)
    serverData["verification"]["verificationRole"]=str(role)
    with open(f"../serverFiles/{guild}.json", 'w') as f:
        json.dump(serverData, f, indent=2)
    return True

def retrieveVerifiedRole(guild):
    with open(f"../serverFiles/{guild}.json") as f:
        serverData = json.load(f)
    return str(serverData["verification"]["verificationRole"])

def getRandomLength(length):
    result_str = ''.join(random.choices(string.ascii_uppercase, k=length))
    return result_str

def generateCaptcha():
    image = ImageCaptcha()
    text=getRandomLength(5)
    image.generate(text)
    image.write(text, 'captcha.png')
    return text