FROM python:3.10-slim

# Установка только необходимых зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала копируем только requirements.txt
COPY requirements.txt .

# Установка зависимостей с обработкой платформо-специфичных пакетов
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pywin32 || true  # Удаляем pywin32 если он был ошибочно установлен

# Копируем остальные файлы проекта
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY html/ /usr/share/nginx/html/

EXPOSE 80