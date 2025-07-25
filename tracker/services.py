import asyncio
import os
from telegram import Bot
import requests

bot = Bot(token=os.getenv('TG_TOKEN'))

async def send_telegram_message(text: str):
    '''
    Отправляет сообщение через телеграм бота
    '''
    response = requests.get('https://api.telegram.org/bot' + os.getenv('TG_TOKEN') + '/getUpdates')
    chat_id = response.json().get('result')[0].get('message').get('chat').get('id')

    try:
        async with Bot(token=os.getenv('TG_TOKEN')) as bot:
            await bot.send_message(chat_id=chat_id, text=text)
            return True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

def sync_send_telegram_message(text: str):
    return asyncio.run(send_telegram_message(text))
