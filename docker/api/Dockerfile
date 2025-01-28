FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY ../../pyproject.toml ../../poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копирование исходного кода и скриптов
COPY ../../src ./src
COPY ../../migrations ./migrations
COPY ../../alembic.ini ./
COPY ../../scripts/entrypoint.sh ./entrypoint.sh

# Установка прав на выполнение скрипта
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]