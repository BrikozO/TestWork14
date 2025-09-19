# Quotes Scraper API

Тестовое задание: асинхронный веб-сервис для парсинга цитат с сайта [quotes.toscrape.com](https://quotes.toscrape.com/) с использованием FastAPI, Celery и MongoDB.

## 🚀 Функциональность

- **API**: Получение цитат с фильтрацией по автору и тегам
- **Дедупликация**: Автоматическое предотвращение дублирования цитат
- **Rate Limiting**: Ограничение частоты запросов парсинга
- **Мониторинг**: Интеграция с Flower для мониторинга Celery задач

## 🏗️ Архитектура

```
├── api/                    # API endpoints
│   └── v1/                
│       └── quotes.py       # Endpoints для работы с цитатами
├── application/            # Application layer
│   ├── controllers/        # Business logic controllers
│   └── dto/               # Data Transfer Objects
├── domain/                # Domain layer
│   ├── models/            # Domain entities
│   └── services/          # Domain services
├── infrastructure/        # Infrastructure layer
│   ├── fastapi_cfg/       # FastAPI configuration
│   └── mongo_db/          # MongoDB repositories
```

## 📋 Требования

- Python 3.12+
- Docker & Docker Compose
- MongoDB 8.0
- Redis 8.2

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd TestWork14
```

### 2. Настройка окружения

Создайте файл `.env` на основе `env.example`:

```bash
cp env.example .env
```

Заполните переменные окружения:

```env
DEBUG=true

MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
MONGO_INITDB_DATABASE=quotes_db

MONGO_URI=mongodb://admin:password123@mongo:27017/
MONGO_DB=quotes_db
MONGO_QUOTES_COLLECTION=quotes

REDIS_URI=redis://redis:6379
```

### 3. Запуск через Docker Compose

```bash
# Сборка и запуск всех сервисов в режиме watch (отслеживания изменений)
docker-compose up --build --watch

# Запуск в фоновом режиме
docker-compose up -d --build
```

### 4. Проверка работы

После запуска будут доступны:

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Flower (Celery monitoring)**: http://localhost:5555
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

## 🔧 API Endpoints

### POST /api/v1/parse-quotes-task

Запускает асинхронную задачу парсинга цитат с сайта.

**Rate Limit**: 1 запрос в 10 минут (предотвращает чрезмерную нагрузку на целевой сайт)

```bash
curl -X POST http://localhost:8000/api/v1/parse-quotes-task
```

**Ответ:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### GET /api/v1/quotes

Получение цитат из базы данных с возможностью фильтрации.

**Параметры запроса:**
- `author` (optional): Фильтр по автору
- `tags` (optional): Фильтр по тегам (можно указать несколько)

**Примеры использования:**

```bash
# Получить все цитаты
curl "http://localhost:8000/api/v1/quotes"

# Фильтр по автору
curl "http://localhost:8000/api/v1/quotes?author=Albert Einstein"

# Фильтр по тегам
curl "http://localhost:8000/api/v1/quotes?tags=inspirational&tags=life"

# Комбинированный фильтр
curl "http://localhost:8000/api/v1/quotes?author=Mark Twain&tags=humor"
```

**Ответ:**
```json
{
  "quotes": [
    {
      "author": "Albert Einstein",
      "text": "Try not to become a person of success, but rather try to become a person of value.",
      "tags": ["adulthood", "success", "value"],
      "parsed_at": "2024-01-15T10:30:00"
    }
  ],
  "filter": {
    "author": "Albert Einstein",
    "tags": []
  },
  "is_empty": false
}
```

## 🗄️ База данных

### MongoDB Коллекция: `quotes`

**Схема документа:**
```json
{
  "author": "string",
  "text": "string", 
  "tags": ["string"],
  "parsed_at": "datetime"
}
```
> [!IMPORTANT]
> Для корректной работы дедупликации создайте в БД необходим индекс по полям author и tags
> В приложении он создается автоматически в lifespan

## 💡 Особенности

### Линтер и форматтер

Настроен и используется быстрый линтер и форматтер `ruff`:

```bash
# Форматирование кода
ruff format .

# Проверка стиля с исправлением ошибок
ruff check . --fix
```

### Rate Limiting
- **Парсинг**: 1 запрос в 10 минут на `/parse-quotes-task` (Можно задать иной лимит в константах)
- **Цель**: Предотвращение чрезмерной нагрузки на целевой сайт
- **Реализация**: SlowAPI, с возможностью интеграции с Redis и работы в распределенном режиме

## 📊 Мониторинг и логи

### Логирование

Все компоненты используют структурированное логирование:

```
[2024-01-15 10:30:00,123 | application.controllers.quotes | INFO]: Parsed 10 quotes from current page. Total: 100
[2024-01-15 10:30:01,456 | infrastructure.mongo_db.quotes_repository | INFO]: Inserted 85 quotes and ignored 15 duplicates
```

### Мониторинг через Flower

- Статус воркеров
- История выполненных задач
- Метрики производительности (скорость выполнения задач)
---

## 🔍 Технические детали

### Стек технологий
- **Backend**: FastAPI, Python 3.12
- **Utils**: Slowapi, Pydantic, httpx
- **Task Queue**: Celery + Redis
- **Database**: MongoDB 8.0
- **Containerization**: Docker + Docker Compose
- **Package Management**: uv
- **Code Quality**: Ruff (linting + formatting)
