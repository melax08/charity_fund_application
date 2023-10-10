# API для работы Благотворительного фонда

## Информация

### Автор:
Илья Малашенко

### Технологический стек:
Python 3.9+, FastAPI, SQLAlchemy, uvicorn, Google Spreadsheets API

### Описание:
В данном проекте присутствует API-сервис для работы благотворительного фонда.

### Возможности:
1. Администрация может создавать проекты и указывать для них количество средств, которые необходимо собрать;
2. Пользователи могут создавать нецелевые пожертвования в фонд, которые будут распределяться между проектами внутри фонда;
3. Присутствует возможность регистрации и авторизации на ресурсе.
4. Администраторы могут сформировать отчет по закрытым проектам фонда в таблицу Google spreadsheets.

## Установка и использование

### Установка:

Клонируйте данный проект и перейдите в каталог с проектом:
```
git clone https://github.com/melax08/charity_fund_application.git && cd charity_fund_application
```
Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv && source venv/bin/activate
```
Установите необходимые зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip && pip install -r requirements.txt
```

Заполните файл .env:
```
mv .env_example .env
vi .env
```

Примените миграции:
```shell
alembic upgrade head
```
### Использование:

Если вам нужно, чтобы приложение автоматически создало супер-пользователя (нужен для работы с множеством эндпоинтов), то заполните в файле `.env` строки:

```shell
FIRST_SUPERUSER_EMAIL=user@example.com
FIRST_SUPERUSER_PASSWORD=ExamplePassword
```

При указании таких параметров при первом запуске приложения будет создан супер-пользователь с логином `user@example.com` и паролем `ExamplePassword`

Для запуска приложения, перейдите в каталог с программой с активированным виртуальным окружением и выполните команду:
```
uvicorn app.main:app
```

Будет запущено приложение по адресу http://127.0.0.1:8000


### Примеры использования API:

Для запущенного API можно посмотреть доступные эндпоинты с описаниями в документации по ссылке: http://127.0.0.1:8000/docs