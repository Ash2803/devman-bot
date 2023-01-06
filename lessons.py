import logging
import os
import time
from textwrap import dedent

import requests
import telegram
from dotenv import load_dotenv


def get_review_information(auth_token, chat_id, bot):
    headers = {
        "Authorization": f'Token {auth_token}'
    }
    params = {
        'timestamp': '',
    }
    while True:
        try:
            response = requests.get(
                "https://dvmn.org/api/long_polling/",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            review_answer = response.json()
            if review_answer['status'] == 'found':
                params['timestamp'] = review_answer['last_attempt_timestamp']
            if review_answer['status'] == 'timeout':
                params['timestamp'] = review_answer['timestamp_to_request']
                continue

            lesson_title = review_answer['new_attempts'][0]['lesson_title']
            lesson_url = review_answer['new_attempts'][0]['lesson_url']
            review_status = review_answer['new_attempts'][0]['is_negative']
            if review_status:
                bot.send_message(chat_id=chat_id, text=dedent(f'''\
                У вас проверили работу "{lesson_title}"
                К сожалению, в работе нашлись ошибки 
                {lesson_url}'''))
            else:
                bot.send_message(chat_id=chat_id, text=dedent(f'''\
                У вас проверили работу "{lesson_title}"
                Преподавателю все понравилось, можно приступать
                к следующему уроку'''))
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
    get_review_information(auth_token, chat_id, bot)


if __name__ == '__main__':
    main()
