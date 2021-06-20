import json

def warn(member, server) -> None:
    with open(f"../serverFiles/{server}.json") as f:
        serverData = json.load(f)
    if str(member) in list(serverData["serverWarns"]):
        serverData["serverWarns"][f"{member}"] += 1

    elif str(member) not in list(serverData["serverWarns"]):
        serverData["serverWarns"][f"{member}"] = 0
        serverData["serverWarns"][f"{member}"] += 1

    with open(f'../serverFiles/{server}.json', 'w') as f:
        json.dump(serverData, f, indent=2)
    return