# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Allure Command Line
RUN wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz \
    && tar -zxvf allure-2.24.1.tgz -C /opt/ \
    && ln -s /opt/allure-2.24.1/bin/allure /usr/local/bin/allure \
    && rm allure-2.24.1.tgz

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Playwright и браузеры
RUN python -m playwright install chromium \
    && playwright install-deps

# Копируем весь проект
COPY . .

# Создаем директории для результатов
RUN mkdir -p allure-results allure-report

# Команда по умолчанию (можно переопределить при запуске)
CMD ["pytest", "--alluredir=allure-results", "-v"]
