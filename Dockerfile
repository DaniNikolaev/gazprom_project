# Dockerfile
FROM python:3.9-slim-buster

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем requirements.txt (или pyproject.toml) и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Команда запуска приложения
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]