from datetime import date, datetime
import json

def log(ctx, type):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f = open(f"../serverLogs/{ctx.guild}.log", "a")
    if type=="message":
        with open(f"../serverFiles/{ctx.guild}.json") as jsonFile:
            serverConfig = json.load(jsonFile)
        if serverConfig["settings"]["logMessages"]:
            f.write(f"\n[{ctx.author} - {time}] - {ctx.content}")
            f.close()
    elif type=="execute":
        f.write(f"\n[{ctx.author} - {time}] executed {ctx.content}")


