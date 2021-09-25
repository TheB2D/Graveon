from datetime import date, datetime
import json, discord

def log(ctx, type, additional=None):
    if ctx.guild == None:
        return
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f = open(f"../serverLogs/{ctx.guild}.log", "a")
    try:
        with open(f"../serverFiles/{ctx.guild}.json") as jsonFile:
            serverConfig = json.load(jsonFile)
        if serverConfig["settings"]["logMessages"]:
            if type == "message":
                f.write(f"\n[{ctx.author} - {ctx.channel} - @{time}] - {ctx.content}")
                f.close()
        if serverConfig["settings"]["logGuild"]:
            if type == "execute":
                f.write(f"\n[{ctx.author} - {time}] executed {ctx.content}")
            elif type == "createChannel":
                f.write(f"\n[EVENT - {time}] created channel \"{ctx.name}\" in category \"{ctx.category}\"")
    except:
        return


