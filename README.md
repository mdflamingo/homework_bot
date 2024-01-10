# Telegram-бот

В этом модуле написан Telegram-бот, который обращается к API сервиса Домашка и узнает статус домашней работы: взята ли домашка на ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Что делает бот:
- раз в 10 минут опрашивать API сервиса Домашка и проверять статус отправленной на ревью домашней работы;
- при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
- логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

Технологии:
- python 3.9,
- python-telegram-bot,
- python-dotenv,
- os,
- sys,
- logging

Установка:
- Клонировать репозиторий:

```git clone https://github.com/mdflamingo/homework_bot.git```

- Перейти в папку с проектом:

```cd homework_bot/```

- Установить виртуальное окружение для проекта:

```python -m venv venv```

- Активировать виртуальное окружение для проекта:

для OS Lunix и MacOS 
```source venv/bin/activate```

для OS Windows
```source venv/Scripts/activate```

- Установить зависимости:

```python3 -m pip install --upgrade pip```

```pip install -r requirements.txt```

- Выполнить миграции на уровне проекта:

```cd yatube```

```python3 manage.py makemigrations```

```python3 manage.py migrate```

- Зарегистрировать чат-бота в Телеграм

- Создать в корневой директории файл .env для хранения переменных окружения

  PRAKTIKUM_TOKEN = 'xxx'
  
  TELEGRAM_TOKEN = 'xxx'
  
  TELEGRAM_CHAT_ID = 'xxx'

- Запустить проект локально:

для OS Lunix и MacOS
```python homework_bot.py```

для OS Windows
```python3 homework_bot.py```

## Автор 
Анастасия Вольнова

