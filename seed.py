import pg8000
from faker import Faker
import random

DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'database': 'task_management',
    'user': 'dashakulikova',  # Правильний користувач!
    'port': 5432
}

fake = Faker('uk_UA')

def seed_users(cursor, num_users=10):
    print(f"📝 Додавання {num_users} користувачів...")
    for i in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)",
            (fullname, email)
        )
    print(f"✅ Додано {num_users} користувачів")

def seed_tasks(cursor, num_tasks=25):
    print(f"📝 Додавання {num_tasks} завдань...")
    
    # Отримуємо ID користувачів та статусів
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cursor.fetchall()]
    
    titles = [
        "Розробити новий функціонал", "Виправити баг", "Написати тести",
        "Оновити документацію", "Провести код-рев'ю", "Налаштувати CI/CD",
        "Оптимізувати базу даних", "Створити API", "Зробити рефакторинг"
    ]
    
    for i in range(num_tasks):
        title = random.choice(titles)
        description = fake.text() if random.choice([True, False]) else None
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )
    
    print(f"✅ Додано {num_tasks} завдань")

def main():
    try:
        conn = pg8000.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        print("🧹 Очищення існуючих даних...")
        cursor.execute("DELETE FROM tasks")
        cursor.execute("DELETE FROM users")
        cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")
        cursor.execute("ALTER SEQUENCE tasks_id_seq RESTART WITH 1")
        
        seed_users(cursor)
        seed_tasks(cursor)
        
        conn.commit()
        
        # Статистика
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks")
        tasks_count = cursor.fetchone()[0]
        
        print("📊 Статистика:")
        print(f"   Користувачів: {users_count}")
        print(f"   Завдань: {tasks_count}")
        
        conn.close()
        print("🎉 Заповнення завершено!")
        
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    main()
