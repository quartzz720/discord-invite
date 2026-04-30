import requests, os, re

TOKEN = os.environ["DISCORD_TOKEN"]
NEOCITIES_KEY = os.environ["NEOCITIES_API_KEY"]

HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}
NEO_HEADERS = {"Authorization": f"Bearer {NEOCITIES_KEY}"}

# Удаляем старые и создаём новый инвайт
requests.delete("https://discord.com/api/v9/users/@me/invites", headers=HEADERS)
r = requests.post("https://discord.com/api/v9/users/@me/invites", headers=HEADERS, json={})
code = r.json()["code"]
url = f"https://discord.gg/{code}"
print(f"Новая ссылка: {url}")

# Скачиваем contact.html с Neocities
page = requests.get(
    "https://neocities.org/api/download?path=contact.html",
    headers=NEO_HEADERS
).text

# Заменяем href у кнопки
new_page = re.sub(
    r'(<a id="invite-btn" href=")[^"]*(")',
    rf'\g<1>{url}\g<2>',
    page
)

# Загружаем обратно
resp = requests.post(
    "https://neocities.org/api/upload",
    headers=NEO_HEADERS,
    files={"contact.html": ("contact.html", new_page.encode("utf-8"), "text/html")}
)
print(resp.json())
