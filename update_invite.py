import requests, json, os

TOKEN = os.environ["DISCORD_TOKEN"]
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}

requests.delete("https://discord.com/api/v9/users/@me/invites", headers=HEADERS)
r = requests.post("https://discord.com/api/v9/users/@me/invites", headers=HEADERS, json={})
code = r.json()["code"]

with open("invite.json", "w") as f:
    json.dump({"url": f"https://discord.gg/{code}"}, f)