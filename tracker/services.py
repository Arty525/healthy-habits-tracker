import asyncio
import os
import time

from telegram import Bot

bot = Bot(token=os.getenv('TG_TOKEN'))

async def send_telegram_message(chat_id: int, text: str)-> bool:
    '''
    Отправляет сообщение через телеграм бота
    '''
    try:
        with Bot(token=os.getenv('TG_TOKEN')) as bot:
            await bot.send_message(chat_id=chat_id, text=text)
            time.sleep(0.5)
            return True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

def sync_send_telegram_message(chat_id: str, text: str):
    return asyncio.run(send_telegram_message(chat_id, text))