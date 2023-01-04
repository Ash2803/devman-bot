import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv


def get_reviews_status(auth_token, chat_id, bot):
    headers = {
        "Authorization": f'Token {auth_token}'
    }
    while True:
        try:
            response = requests.get("https://dvmn.org/api/long_polling/", headers=headers, timeout=5)
            response.raise_for_status()
            timestamp = response.json()['new_attempts'][0]['timestamp']
            lesson_title = response.json()['new_attempts'][0]['lesson_title']
            lesson_url = response.json()['new_attempts'][0]['lesson_url']
            review_status = response.json()['new_attempts'][0]['is_negative']
            params = {
                'timestamp': timestamp
            }
            if review_status:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson_title}"\n'
                                                       f'К сожалению, в работе нашлись ошибки\n'
                                                       f'{lesson_url}')
            else:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson_title}"\n'
                                                       f'Преподавателю все понравилось, можно приступать'
                                                       f'к следующему уроку')
            new_response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers=headers,
                params=params,
                timeout=5
            )
            new_response.raise_for_status()
            new_lesson_title = new_response.json()['new_attempts'][0]['lesson_title']
            new_lesson_url = new_response.json()['new_attempts'][0]['lesson_url']
            new_review_status = new_response.json()['new_attempts'][0]['is_negative']
            if new_review_status:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{new_lesson_title}"\n'
                                                       f'К сожалению, в работе нашлись ошибки\n'
                                                       f'{new_lesson_url}')
            else:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{new_lesson_title}"\n'
                                                       f'Преподавателю все понравилось, можно приступать'
                                                       f'к следующему уроку')
        except requests.exceptions.ReadTimeout:
            logging.exception('Request timed out')
            continue
        except requests.exceptions.ConnectionError:
            logging.exception('Connection lost. Reconnecting...')
            time.sleep(10)
            continue


def main():
    load_dotenv()
    auth_token = os.environ['AUTH_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)
    get_reviews_status(auth_token, chat_id, bot)


if __name__ == '__main__':
    main()