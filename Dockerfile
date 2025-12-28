# Используем стабильный образ на основе Debian 11 (Bullseye)
FROM python:3.10-bullseye

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium \
    openjdk-11-jre-headless \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Проверка установки Chromium
RUN chromium --version

# Настройка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CHROMIUM_BIN=/usr/bin/chromium
ENV PLAYWRIGHT_BROWSERS_PATH=0

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Playwright и Chromium
RUN python -m playwright install chromium

# Копируем весь код проекта
COPY . .

# Точка входа по умолчанию
CMD ["pytest", "tests/", "--alluredir=allure-results", "-v"]