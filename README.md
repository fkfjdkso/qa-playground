# QA Playground — Pet Project for Junior AQA

[![QA Playground](https://github.com/fkfjdkso/qa-playground/actions/workflows/ci_pipeline.yml/badge.svg)](https://github.com/fkfjdkso/qa-playground/actions/workflows/ci_pipeline.yml)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pytest](https://img.shields.io/badge/Pytest-tested-green)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-teal)
![Allure](https://img.shields.io/badge/Allure-report-orange)
[Отчет Allure](https://fkfjdkso.github.io/qa-playground/)

---

## О проекте

Учебный проект по автоматизации тестирования (AQA Python).

Проект представляет собой веб-приложение для поиска локаций по стране и почтовому индексу (ZIP-коду), сохранения результатов в базу данных и проверки поведения системы в различных сценариях, включая намеренно внедрённые дефекты.

---

## Что демонстрирует проект

- UI-автоматизация тестирования
- API тестирование
- Работа с базой данных
- Проверка негативных сценариев и дефектов
- Контейнеризация окружения
- CI/CD пайплайн (GitHub Actions)
- Генерация отчетов Allure

---

## Цели проекта

Проект создан в рамках обучения автоматизации тестирования для демонстрации навыков работы с:

- UI тестированием
- API тестированием
- базами данных
- тестовой инфраструктурой (Docker + CI)

---

## Стек технологий

### Backend

- Python
- FastAPI
- REST API

### Frontend

- HTML
- CSS
- JavaScript

### Database

- PostgreSQL (Neon / локально через Docker)
- SQLAlchemy 2.0

### Тестирование

- Pytest
- Selenium (Chrome WebDriver)
- Requests (API testing)
- SQLAlchemy (DB validation)

### CI/CD и отчётность

- GitHub Actions
- Docker / Docker Compose
- Allure Reports
- GitHub Pages (публикация отчётов)

---

## Архитектура проекта

```
qa-playground/
├── .github/workflows/       # GitHub Actions пайплайны
│   └── ci_pipeline.yml      # Твой переименованный конфиг CI
├── app/                     # Исходный код приложения
│   ├── static/              # Frontend (HTML, CSS, JS)
│   ├── database.py          # Подключение к БД и сессии
│   ├── main.py              # FastAPI роуты и логика багов
│   └── model.py             # SQLAlchemy модель
├── pages/                   # Слой Page Object (UI-тесты)
├── screenshots/             # Скриншоты отчетов и багов
├── tests/                   # Автотесты
├── Dockerfile               # Инструкции по сборке образа
├── docker-compose.yml       # Конфиг для запуска прилы и БД
├── requirements.txt         # Зависимости проекта
└── README.md                # Документация
```

---

## Функционал приложения

### Поиск локаций

Пользователь вводит:

- страну
- почтовый индекс

Система возвращает:

- город

---

### Сохранение данных

Результаты поиска можно сохранить в базу данных.

---

## Панель дефектов (test fault injection)

В приложение добавлена панель переключаемых дефектов для тестирования устойчивости системы.

### 1. Медленный ответ базы данных

Искусственная задержка обработки запросов.

Используется для проверки таймаутов и деградации производительности.

---

### 2. Повреждение данных

Название города обрезается до первых 3 символов.

Пример:
Мурманск → Мур

---

### 3. Ошибка обработки дубликатов

Два режима:

- корректный: проверка дубликатов на сервере → 400 Bad Request
- некорректный: отключена серверная проверка → защита только на уровне БД (primary key) → 409 Conflict

---

### 4. Ghost-кнопка отправки

Кнопка UI не отправляет запрос на сервер.

Используется для проверки UI-логики и событий.

---

## Автотесты

Всего: 18 тестов

- UI: 5 тестов
- API + DB: 8 тестов
- параметризованные сценарии включены

---

## UI тесты (Selenium)

Используемые инструменты:

- Selenium
- Pytest
- Page Object Model
- Allure

### Сценарии:

- корректное отображение локации
- сохранение в БД
- проверка дубликатов
- поведение при медленном ответе сервера
- ghost button

---

## API и DB тесты

Используемые инструменты:

- Requests
- SQLAlchemy
- Pytest
- Allure

### Сценарии:

- получение локации (валидные входные данные)
- сохранение в БД
- проверка обрезки данных (bug simulation)
- проверка дубликатов
- негативные сценарии (пустой ввод, неверный индекс)
- проверка очистки тестовых данных

---

## CI/CD (GitHub Actions)

Пайплайн:

- при push запускаются тесты
- поднимается Docker Compose окружение
- запускается приложение и база данных
- выполняются UI/API/DB тесты
- генерируется Allure отчет
- отчет публикуется через GitHub Pages

---

## Allure Reports

После прогона тестов:

- формируется `allure-results`
- генерируется HTML отчет
- публикуется автоматически в GitHub Pages
- доступен без локального запуска проекта

---

## Тестовая документация

В проекте также присутствуют:

- тест-кейсы
- тест-план
- баг-репорты

---

## Пример найденного дефекта

В процессе тестирования был найден и задокументирован дефект.

Баг-репорт включает:

- описание
- шаги воспроизведения
- ожидаемый и фактический результат
- окружение
- приоритет и severity
- вложения

---

## Запуск проекта

### Клонирование

```bash
git clone https://github.com/fkfjdkso/qa-playground.git
cd qa-playground
```

# Установка зависимостей

```bash
pip install -r requirements.txt
```

# Настройка БД

Создать `.env`:

```
USER=...
PASSWORD=...
HOST=...
PORT=...
DB=...
```

### Запуск приложения

```bash
uvicorn app.main:app
```

---

## Запуск тестов

### UI тесты

```bash
pytest tests/test_ui.py -v
```

### API тесты

```bash
pytest tests/test_api.py -v
```

### Генерация отчета Allure

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Ключевые навыки QA

### Тест-дизайн

- Позитивные и негативные сценарии
- Граничные значения
- Анализ требований

### API и backend тестирование

- REST API проверки
- Статус-коды
- Контрактные проверки

### Работа с базами данных

- SQLAlchemy
- Проверка состояния данных
- Валидация после операций

### UI-автоматизация

- Selenium WebDriver
- Page Object Model
- Работа с динамическими элементами

### CI/CD

- GitHub Actions
- Docker Compose
- Автоматический запуск тестов
- Публикация отчетов

### Отчетность

- Allure Reports
- Шаги тестов
- Анализ результатов

---

## Визуализация результатов

### Интерфейс приложения

![Application UI](./screenshots/main.png)

### Отчет Allure

![Allure Report](./screenshots/allure1.png)
![Allure Report](./screenshots/allure2.png)

---

### Тестовая документация

![Test Documentation](./screenshots/testcases.png)
![Test Documentation](./screenshots/testplan.png)
![Test Documentation](./screenshots/bugreport.png)

---

### Тестирование API в Postman

![Postman Collection](./screenshots/postman1.png)
![Postman Collection](./screenshots/postman2.png)
![Postman Collection](./screenshots/postman3.png)

---

## Примечание

Проект создан в рамках обучения автоматизации тестирования и предназначен для демонстрации практических навыков работы с UI, API и базами данных.
