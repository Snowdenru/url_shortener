# URL Shortener API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

Простое API для сокращения URL-адресов, построенное на FastAPI с использованием SQLite в качестве базы данных.

## 📌 Возможности

- 🔗 Создание коротких ссылок из длинных URL
- ⏱️ Установка срока действия ссылки (опционально)
- ✏️ Пользовательские короткие коды (опционально)
- 📊 Статистика переходов по ссылкам
- 🔄 Автоматическое перенаправление
- 📄 Автоматическая документация API (Swagger/OpenAPI)

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8+
- pip

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## 📚 Документация API

После запуска приложения документация API будет доступна:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🛠️ Использование API

### Создание короткой ссылки

**Запрос:**
```bash
POST /shorten
Content-Type: application/json

{
  "original_url": "https://example.com/very-long-url",
  "custom_code": "my-link",  # опционально
  "expiry_days": 7           # опционально
}
```

**Ответ:**
```json
{
  "original_url": "https://example.com/very-long-url",
  "short_code": "my-link",
  "clicks": 0,
  "created_at": "2025-08-06T12:00:00",
  "expires_at": "2025-08-13T12:00:00",
  "is_active": true
}
```

### Перенаправление по короткой ссылке

Перейдите по:
```
GET /my-link
```
Вы будете автоматически перенаправлены на оригинальный URL.

### Получение статистики

**Запрос:**
```bash
GET /stats/my-link
```

**Ответ:**
```json
{
  "original_url": "https://example.com/very-long-url",
  "short_code": "my-link",
  "clicks": 42,
  "created_at": "2025-08-06T12:00:00",
  "expires_at": "2025-08-13T12:00:00",
  "is_active": true
}
```

## � Структура базы данных

Таблица `urls`:
| Поле | Тип | Описание |
|------|------|------------|
| id | INTEGER | Первичный ключ |
| original_url | TEXT | Оригинальный URL |
| short_code | TEXT | Уникальный короткий код |
| clicks | INTEGER | Количество переходов |
| created_at | DATETIME | Дата создания |
| expires_at | DATETIME | Дата истечения срока |
| is_active | BOOLEAN | Активна ли ссылка |

## 🛠️ Разработка

### Запуск тестов
```bash
pytest
```

### Форматирование кода
```bash
black .
```

### Проверка стиля кода
```bash
flake8
```

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.

---

Разработано с ❤️ для упрощения работы с URL-адресами