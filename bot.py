import discord
import requests
import asyncio
from flask import Flask
from threading import Thread

# --- МИКРО-СЕРВЕР ---
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- ФУНКЦИЯ САМОПИНГА ---
async def self_ping(url):
    while True:
        try:
            requests.get(url)
            print("Сделал самопинг!")
        except:
            print("Ошибка самопинга")
        await asyncio.sleep(600) # Пингуем раз в 10 минут

TOKEN = 'MTQ5MDI0NDIwOTc0NjI1MTc5Ng.Gk3Rzm.hTgqB5QHxCS5ZNA-16WGUZN8xUHSk_pAv3jV2g' # Вставь новый токен, если Discord его опять сбросил
IP = '8523423186'
PORT = '28015'
# Скопируй ссылку из Render (синяя под названием проекта, кончается на .onrender.com)
MY_URL = 'https://rust-bot-xhgc.onrender.com' 

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Бот {client.user} запущен!')
    keep_alive()
    # Запускаем самопинг в фоновом режиме
    client.loop.create_task(self_ping(MY_URL))
    
while True:
        try:
            # Используем альтернативное API (оно более стабильное)
            response = requests.get(f"https://api.battlemetrics.com/servers?filter[search]={IP}")
            data = response.json()
            
            # Проверяем, нашел ли BattleMetrics сервер
            if data['data']:
                server = data['data'][0]['attributes']
                status = f"Онлайн: {server['players']}/{server['maxPlayers']}"
            else:
                status = "Сервер не найден"
                
            await client.change_presence(activity=discord.Game(name=status))
            print(f"Обновил статус: {status}")
        except Exception as e:
            print(f"Ошибка: {e}")
            await client.change_presence(activity=discord.Game(name="Ошибка API"))
            
        await asyncio.sleep(60)

client.run(TOKEN)
