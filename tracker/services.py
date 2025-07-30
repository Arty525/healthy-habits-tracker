import os
import requests


def send_telegram_message(chat_id: str, text: str):
    """Отправляет сообщение через телеграм"""
    params = {
        "text": text,
        "chat_id": chat_id,
    }

    requests.get(
        f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}/sendMessage',
        params=params,
    )


def get_tg_chat_id(telegram_id: str):
    """Запрашивает у telegram chat_id пользователя"""
    result = requests.get(
        f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}/getUpdates'
    ).json().get('result')
    for r in result:
        if r.get('message').get('chat').get('username') == telegram_id:
            return r.get('message').get('chat').get('id')
    return None
