

# Управление продуктам API


## Технологии

- **FastAPI** — фреймворк для разработки высокопроизводительных API.
- **PostgreSQL** — реляционная база данных.
- **SQLAlchemy** — ORM для взаимодействия с базой данных.
- **Docker** — контейнеризация приложения для легкого развёртывания и запуска.

## Основные возможности

- Добавление новых продуктов
- Обновление информации о продуктах
- Удаление продуктов
- Получение информации о продуктах
- Фильтрация продуктов по категории и диапазону цен
- Автоматическая документация API с использованием Swagger

## Установка и запуск


1. Запустите Docker Compose для сборки образов и запуска контейнеров:

   ```bash
   docker-compose up --build
   ```

   Docker Compose создаст и запустит контейнеры для FastAPI и PostgreSQL. API будет доступно по адресу [http://localhost:8000](http://localhost:8000).


## Использование API

### Документация API

- **Swagger UI**: После запуска API документация доступна по адресу [http://localhost:8000/docs](http://localhost:8000/docs).

### Основные эндпоинты

- **GET** `/api/products` — Получение списка продуктов с поддержкой фильтров.
- **GET** `/api/products/{id}` — Получение информации о продукте по ID.
- **POST** `/api/products` — Добавление нового продукта.
- **PUT** `/api/products/{id}` — Обновление информации о продукте.
- **DELETE** `/api/products/{id}` — Удаление продукта.

### Примеры запросов

#### Получить все продукты

```http
GET /api/products
```

#### Фильтрация по категории и диапазону цен

```http
GET /api/products?category=Tools&min_price=10&max_price=100
```

#### Добавление нового продукта

```http
POST /api/products
Content-Type: application/json

{
  "id": 1,
  "product_title": "Молоток",
  "category": "инструменты",
  "price": 15.0,
  "description": "Молоток для строительных работ"
}
```

#### Обновление продукта

```http
PUT /api/products/1
Content-Type: application/json

{
  "product_title": "Молоток",
  "category": "инструменты",
  "price": 17.0,
  "description": "Обновленное описание молотка"
}
```

#### Удаление продукта

```http
DELETE /api/products/1
```

## Структура проекта

```plaintext
.
├── app.py
├── database_handler.py
├── docker-compose.yml
├── dockerfile
├── models.py
├── public
│   └── index.html
├── readme.md
└── requirements.txt

```

## Переменные окружения

Для конфигурации приложения можно использовать переменные окружения, задаваемые в `docker-compose.yml`:

- `DATABASE_URL`: URL для подключения к PostgreSQL (формат: `postgresql://username:password@db:5432/mydatabase`).
