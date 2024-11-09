import time
import random
from pyrogram import Client, filters
from pyrogram.types import Message

# Чтение конфигураций
with open("api_ids", "r") as f:
    app_id, hash_id = f.read().strip().split("\n")

with open("text.txt", "r", encoding="utf-8") as f:
    spam_texts = [line.strip() for line in f if line.strip()]

# Чтение чатов для спама
with open("id.txt", "r") as f:
    chat_ids = [line.strip() for line in f.readlines()]

# Создание клиента Pyrogram
app = Client("spammer", api_id=app_id, api_hash=hash_id)

# Функция для отправки спама
async def send_spam():
    while True:
        spam_text = random.choice(spam_texts)  # Выбираем случайное сообщение
        for chat_id in chat_ids:
            try:
                print(f"Отправляю сообщение в чат {chat_id}...")
                await app.send_message(chat_id, spam_text)
                print(f"Сообщение отправлено в {chat_id}")
            except Exception as e:
                print(f"Ошибка при отправке в {chat_id}: {e}")
        print("Задержка 60 секунд перед следующим сообщением...")
        time.sleep(60)  # Задержка 60 секунд

# Обработчик команды /sp
@app.on_message(filters.command("sp"))
async def start_spam(client, message: Message):
    print(f"Команда /sp получена от пользователя {message.from_user.id} в чате {message.chat.id}")
    await message.reply("Начинаю спам во всех указанных чатах...")
    await send_spam()

# Проверка подключения
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    print("Бот успешно запущен и подключен к Telegram!")

# Запуск бота
app.run()
