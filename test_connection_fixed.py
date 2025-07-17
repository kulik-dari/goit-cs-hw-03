import pg8000
import pymongo
import getpass

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
        }
    ]
    
    for config in connection_attempts:
        try:
            print(f"Спроба підключення як {config['name']}...")
            
            # Правильний синтаксис для pg8000
            if 'password' in config:
                conn = pg8000.connect(
                    host=config['host'],
                    database=config['database'],
                    user=config['user'],
                    password=config['password'],
                    port=config['port']
                )
            else:
                conn = pg8000.connect(
                    host=config['host'],
                    database=config['database'],
                    user=config['user'],
                    port=config['port']
                )
            
            # Тестовий запит
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            result = cursor.fetchone()
            print(f"✅ PostgreSQL ({config['name']}): {result[0][:50]}...")
            
            conn.close()
            return config
            
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
    print("🧪 Тестування підключень (виправлена версія)...")
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
                
        print("\n🚀 Можна створювати таблиці!")
    else:
        print("💥 PostgreSQL все ще не працює")
        
    if not mongo_ok:
        print("⚠️  Запустіть MongoDB в новому терміналі:")
        print("   mkdir -p ~/data/db")
        print("   mongod --dbpath ~/data/db")
