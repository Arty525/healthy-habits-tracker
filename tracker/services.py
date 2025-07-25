import asyncio
import os

from kombu.asynchronous.http import Response
from telegram import Bot


async def send_telegram_message(chat_id: int, text: str)-> bool:
    '''
    Отправляет сообщение через телеграм бота
    '''
    try:
        bot = Bot(token=os.getenv('TG_TOKEN'))
        await bot.send_message(chat_id=chat_id, text=text)
        return True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

def sync_send_telegram_message(chat_id: str, text: str):
    return asyncio.run(send_telegram_message(chat_id, text))

async def _async_send_telegram_message(chat_id: str, text: str) -> None:
    """Асинхронная отправка сообщения"""
    bot = Bot(token=os.getenv('TG_TOKEN'))
    await bot.send_message(chat_id=chat_id, text=text)