import pg8000

DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'database': 'postgres',
    'user': 'dashakulikova',  # Правильний користувач!
    'port': 5432
}

def create_database():
    try:
        conn = pg8000.connect(**DATABASE_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Перевіряємо існування бази
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'task_management'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE task_management")
            print("✅ База даних 'task_management' створена!")
        else:
            print("ℹ️  База даних 'task_management' вже існує.")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Помилка при створенні БД: {e}")

def create_tables():
    try:
        # Підключаємося до task_management
        config = DATABASE_CONFIG.copy()
        config['database'] = 'task_management'
        
        conn = pg8000.connect(**config)
        cursor = conn.cursor()
        
        # Створюємо таблиці
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            )
        """)
        print("✅ Таблиця users створена")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS status (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        print("✅ Таблиця status створена")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                status_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("✅ Таблиця tasks створена")
        
        # Додаємо статуси
        cursor.execute("""
            INSERT INTO status (name) VALUES 
            ('new'), ('in progress'), ('completed')
            ON CONFLICT (name) DO NOTHING
        """)
        print("✅ Початкові статуси додані")
        
        conn.commit()
        conn.close()
        print("🎉 Всі таблиці створені успішно!")
        
    except Exception as e:
        print(f"❌ Помилка при створенні таблиць: {e}")

def main():
    print("🏗️  Створення бази даних та таблиць...")
    create_database()
    create_tables()
    print("✅ Процес завершено!")

if __name__ == "__main__":
    main()
