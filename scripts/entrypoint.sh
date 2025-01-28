#!/bin/bash
set -e

# Установка netcat для проверки доступности базы данных
apt-get update && apt-get install -y netcat-openbsd

# Ожидание доступности базы данных
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database is ready!"

# Применение миграций
echo "Running migrations..."
alembic upgrade head

echo "Migrations completed!"

# Запуск основного приложения
echo "Starting application..."
exec "$@"