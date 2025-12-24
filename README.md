Автоматизация тестирования логина Saucedemo

Автоматизированные UI-тесты для сайта [https://www.saucedemo.com/](https://www.saucedemo.com/) с использованием **Playwright**, **Page Object** и **Allure**.

Тесты покрывают 5 основных сценариев авторизации:
1. Успешный логин (`standard_user` / `secret_sauce`)
2. Логин с неверным паролем
3. Логин заблокированного пользователя (`locked_out_user`)
4. Логин с пустыми полями
5. Логин пользователем `performance_glitch_user`

---

Для запуска тестов

1. Клонировать репозиторий
2. Установить зависимости
3. Запустить тесты и сбор результатов. Из корневой папки через терминал командой python -m pytest tests/ --alluredir=./allure-results -v
4. Сгенерировать отчет Allure командой allure generate allure-results -o allure-report --clean в теринале
5. Открыть отчет в браузере командой allure open allure-report 

