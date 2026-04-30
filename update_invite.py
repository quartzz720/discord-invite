import requests, json, os, re

TOKEN = os.environ["DISCORD_TOKEN"]
NEOCITIES_KEY = os.environ["NEOCITIES_API_KEY"]

HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}

# Удаляем старые и создаём новый инвайт
requests.delete("https://discord.com/api/v9/users/@me/invites", headers=HEADERS)
r = requests.post("https://discord.com/api/v9/users/@me/invites", headers=HEADERS, json={})
code = r.json()["code"]
url = f"https://discord.gg/{code}"
print(f"Новая ссылка: {url}")

# Скачиваем contact.html с Neocities
page = requests.get(
    "https://neocities.org/api/download?sitename=koiayame&filename=contact.html",
    headers={"Authorization": f"Bearer {NEOCITIES_KEY}"}
).text

# Заменяем href у кнопки
new_page = re.sub(
    r'(<a id="invite-btn" href=")[^"]*(")',
    rf'\g<1>{url}\g<2>',
    page
)

# Загружаем обратно
requests.post(
    "https://neocities.org/api/upload",
    headers={"Authorization": f"Bearer {NEOCITIES_KEY}"},
    files={"contact.html": ("contact.html", new_page, "text/html")}
)
print("Сайт обновлён!")
