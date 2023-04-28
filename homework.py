import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import StatusCodeError

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяет доступность переменных окружения."""
    ENV_VARIABLES = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    for var in ENV_VARIABLES:
        if var is None:
            logger.critical(
                f'Отсутствует обязательная переменная окружения: {var}.'
                f'Программа принудительно остановлена.'
            )
    return all(ENV_VARIABLES)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'сообщение {message} отправлено в чат.')
    except Exception as error:
        logger.error(f'Ошибка при отправке сообщения{message}: {error}.')


def get_api_answer(timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            raise StatusCodeError(f'Неожиданный статус код:'
                                  f'{response.status_code}.')
        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error(f'API {ENDPOINT} недоступен! Ошибка: {error}.')


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        logger.error(f'Тип данных {response} не соответствует документации.')
        raise TypeError
    for key in ['homeworks', 'current_date']:
        if key not in response:
            logger.error(f'Oтсутствует ожидаемый ключ {key} в ответе API.')
            raise KeyError
    homework = response.get('homeworks')
    if not isinstance(homework, list):
        logger.error(f'Тип данных {homework} не соответствует документации.')
        raise TypeError
    return homework


def parse_status(homework):
    """Получает информацию о статусе работы."""
    if 'homework_name' not in homework:
        raise KeyError
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status in HOMEWORK_VERDICTS:
        verdict = HOMEWORK_VERDICTS[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    logger.error(f'Неожиданный статус домашней работы: {homework_status}')
    raise KeyError


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        sys.exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            if len(homework) > 0:
                send_message(bot, parse_status(homework[0]))
            send_message(bot, 'Работу не взяли на проверку')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(bot, message)
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
