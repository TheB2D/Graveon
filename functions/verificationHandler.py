import json
import random
import string
from functions import utils
from captcha.image import ImageCaptcha

def setVerificationChannel(id, channelID, guild) -> None:
    serverData = utils.openFile(guild)
    serverData["verification"]["verificationChannelID"] = channelID
    serverData["verification"]["verificationID"] = id
    with open(f'../serverFiles/{guild}.json', 'w') as f:
        json.dump(serverData, f, indent=2)
    return

def bindVerification(user, code, guild=None) -> bool:
    with open("../functions/temporary/verificationBinds.json") as f:
        cache = json.load(f)
    if guild!=None:
        cache["verificationBinds"][f"{user}"]=[code, str(guild)]
    else:
        cache["verificationBinds"][f"{user}"][0]=code
    with open("../functions/temporary/verificationBinds.json", 'w') as f:
        json.dump(cache, f, indent=2)
    return True

def setVerificationRole(role, guild) -> bool:
    serverData = utils.openFile(guild)
    serverData["verification"]["verificationRole"]=str(role)
    with open(f"../serverFiles/{guild}.json", 'w') as f:
        json.dump(serverData, f, indent=2)
    return True

def retrieveVerifiedRole(guild):
    serverData = utils.openFile(guild)
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