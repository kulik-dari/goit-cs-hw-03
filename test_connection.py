import pg8000.native as pg8000
import pymongo
import getpass
import os

def test_postgresql():
    """Тестуємо різні способи підключення до PostgreSQL"""
    username = getpass.getuser()
    
    connection_attempts = [
        # Спроба 1: з postgres користувачем
        {
            'host': 'localhost',
            'database': 'postgres',
            'user': 'postgres',
            'password': 'test123',
            'port': 5432,
            'name': 'postgres user'
        },
        # Спроба 2: з вашим користувачем
        {
            'host': 'localhost',
            'database': 'postgres',
            'user': username,
            'port': 5432,
            'name': f'{username} user'
        },
        # Спроба 3: з вашим користувачем і базою
        {
            'host': 'localhost',
            'database': username,
            'user': username,
            'port': 5432,
            'name': f'{username} user and database'
        }
    ]
    
    for config in connection_attempts:
        try:
            print(f"Спроба підключення як {config['name']}...")
            
            # Підключаємося
            if 'password' in config:
                conn = pg8000.connect(**config)
            else:
                conn = pg8000.connect(
                    host=config['host'],
                    database=config['database'],
                    user=config['user'],
                    port=config['port']
                )
            
            # Тестовий запит
            result = conn.run("SELECT version()")
            print(f"✅ PostgreSQL ({config['name']}): {result[0][0][:50]}...")
            
            # Зберігаємо робочу конфігурацію
            working_config = config.copy()
            conn.close()
            return working_config
            
        except Exception as e:
            print(f"❌ PostgreSQL ({config['name']}): {e}")
    
    return None

def test_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB: підключення успішне!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ MongoDB: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Тестування підключень...")
    print("=" * 50)
    
    # Тестуємо PostgreSQL
    pg_config = test_postgresql()
    
    print("\n" + "=" * 50)
    
    # Тестуємо MongoDB
    mongo_ok = test_mongodb()
    
    print("=" * 50)
    
    if pg_config:
        print("🎉 PostgreSQL ПРАЦЮЄ!")
        print("Робоча конфігурація:")
        for key, value in pg_config.items():
            if key != 'name':
                print(f"  {key}: {value}")
        
        # Створюємо файл конфігурації
        with open('working_config.py', 'w') as f:
            f.write("# Робоча конфігурація PostgreSQL\n")
            f.write("DATABASE_CONFIG = {\n")
            for key, value in pg_config.items():
                if key != 'name':
                    if isinstance(value, str):
                        f.write(f"    '{key}': '{value}',\n")
                    else:
                        f.write(f"    '{key}': {value},\n")
            f.write("}\n")
        
        print("\n💾 Конфігурація збережена в working_config.py")
        
        if mongo_ok:
            print("🎉 MongoDB ПРАЦЮЄ!")
            print("\n🚀 ВСЕ ГОТОВО! Можна запускати завдання!")
        else:
            print("⚠️  MongoDB потрібно запустити окремо")
            print("   Команда: mongod --dbpath ~/data/db")
    else:
        print("💥 PostgreSQL не працює. Спробуйте перевстановити:")
        print("   brew uninstall postgresql@14")
        print("   brew install postgresql@14")
        print("   brew services start postgresql@14")
