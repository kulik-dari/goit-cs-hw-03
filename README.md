# goit-cs-hw-03
# Домашнє завдання 3 - Системи управління базами даних

Це домашнє завдання складається з двох частин:
1. **Завдання 1**: Робота з PostgreSQL - система управління завданнями
2. **Завдання 2**: Робота з MongoDB - система управління котами

## 📋 Структура проєкту

```
goit-cs-hw-03/
├── create_tables.py    # Скрипт створення таблиць PostgreSQL
├── seed.py            # Скрипт заповнення таблиць тестовими даними
├── queries.py         # Python скрипт з SQL запитами
├── queries.sql        # SQL файл з запитами
├── main.py           # CRUD операції для MongoDB
├── requirements.txt   # Залежності проєкту
└── README.md         # Цей файл
```

## 🚀 Запуск завдань

### Завдання 1: PostgreSQL

#### 1. Створення таблиць:
```bash
python3 create_tables.py
```

#### 2. Заповнення тестовими даними:
```bash
python3 seed.py
```

#### 3. Виконання SQL запитів:
```bash
python3 queries.py
```

Альтернативно, можна виконати запити безпосередньо в PostgreSQL:
```bash
psql -U your_username -d task_management -f queries.sql
```

### Завдання 2: MongoDB

```bash
python3 main.py
```

Програма запустить інтерактивне меню для виконання CRUD операцій.

## 📊 Опис завдань

### Завдання 1: PostgreSQL
- **База даних**: `task_management`
- **Таблиці**: `users`, `status`, `tasks`
- **Функціонал**: 14 різних SQL запитів для роботи із завданнями

### Завдання 2: MongoDB
- **База даних**: `cats_database`
- **Колекція**: `cats`
- **Функціонал**: CRUD операції через інтерактивне меню

## 🛠️ Технології

- **Python 3.8+**
- **PostgreSQL 12+**
- **MongoDB 4.4+**
- **Бібліотеки**:
  - `psycopg2-binary` - для роботи з PostgreSQL
  - `pymongo` - для роботи з MongoDB
  - `Faker` - для генерації тестових даних

