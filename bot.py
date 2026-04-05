import discord
from discord.ext import tasks
import requests

# --- НАСТРОЙКИ (ЗАПОЛНИ ИХ) ---
TOKEN = 'MTQ5MDI0NDIwOTc0NjI1MTc5Ng.Gk3Rzm.hTgqB5QHxCS5ZNA-16WGUZN8xUHSk_pAv3jV2g'    # Сюда вставь токен из Discord Developer Portal
IP = '85.234.23.186'          # IP твоего сервера Rust
PORT = '28015'                # Query порт сервера
# ------------------------------

client = discord.Client(intents=discord.Intents.all())

@tasks.loop(seconds=30)
async def update_info():
    try:
        # Опрос сервера через API мониторинга
        url = f"https://api.mcsrvstat.us/2/{IP}:{PORT}"
        data = requests.get(url).json()

        if data.get("online"):
            current = data["players"]["online"]
            maximum = data["players"]["max"]
            status = f"{current}/{maximum} заходят 0"
        else:
            status = "Сервер выключен"

        # Установка статуса
        await client.change_presence(activity=discord.Game(name=status))
        print(f"Статус обновлен: {status}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

@client.event
async def on_ready():
    print(f"Бот {client.user} запущен и работает!")
    update_info.start()

client.run(TOKEN)

