## Запуск приложения

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/oleg-rybakov/telegram_bot.git
```

### 2. Создайте файл .env по примеру .env.example и заполните его корректными данными, где:

* POSTGRES_USER - имя пользователя БД
* POSTGRES_PASSWORD - пароль пользователя БД
* POSTGRES_DB - имя базы данных
* DATABASE_URL - строка подключения к базе данных
* BOT_TOKEN - токен телеграм-бота
* IMEI_CHECK_API_KEY_SANDBOX - токен для проверки IMEI с помощью сервиса imeicheck.net в режиме SANDBOX
* IMEI_CHECK_API_KEY_LIVE - токен для проверки IMEI с помощью сервиса imeicheck.net в режиме LIVE

### 3. Запустите приложение с помощью команды

```bash
docker-compose up -d
```

Эта команда запустит все сервисы приложения в фоновом режиме, а именно:

- База данных PostgreSQL
- Приложение FastAPI
- Телеграм-бот

и применит миграции БД (создаст таблицу users).

### 4. Проверьте, что приложение запущено и доступно по адресу http://localhost:8000/docs

### 5. Заполните базу данных, внеся в нее Telegram ID пользователей, входящи в белый список. Для этого выполните команду:

```bash
# Войдите в контейнер БД и подключитесь к ней
docker compose exec db psql -U <POSTGRES_USER> -d <POSTGRES_DB>

# Выполните запрос на вставку данных
INSERT INTO users (tg_id) VALUES (123456789, 987654321);
```

где <POSTGRES_USER> и <POSTGRES_DB> - соответствующие значения из файла .env.
а 123456789, 987654321 - Telegram ID пользователей, которых необходимо включить в белый список. 
