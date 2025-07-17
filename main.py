from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from bson import ObjectId
import sys

# Налаштування підключення до MongoDB
MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "cats_database"
COLLECTION_NAME = "cats"

class CatsDatabase:
    def __init__(self):
        """Ініціалізація підключення до MongoDB"""
        try:
            self.client = MongoClient(MONGODB_URL)
            # Перевіряємо підключення
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            print("✅ Підключення до MongoDB встановлено успішно!")
        except ConnectionFailure as e:
            print(f"❌ Помилка підключення до MongoDB: {e}")
            print("   Запустіть MongoDB: mongod --dbpath ~/data/db")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Непередбачена помилка: {e}")
            sys.exit(1)

    def create_sample_data(self):
        """Створює приклади котів у базі даних"""
        try:
            # Перевіряємо, чи є вже дані
            if self.collection.count_documents({}) == 0:
                sample_cats = [
                    {
                        "name": "barsik",
                        "age": 3,
                        "features": ["ходить в капці", "дає себе гладити", "рудий"]
                    },
                    {
                        "name": "murka",
                        "age": 2,
                        "features": ["полює на мишей", "любить рибу", "сіра"]
                    },
                    {
                        "name": "felix",
                        "age": 5,
                        "features": ["спить весь день", "любить молоко", "чорний"]
                    },
                    {
                        "name": "fluffy",
                        "age": 1,
                        "features": ["дуже пухнастий", "грається з клубком", "білий"]
                    }
                ]
                
                result = self.collection.insert_many(sample_cats)
                print(f"✅ Створено {len(result.inserted_ids)} котів у базі даних")
            else:
                print("ℹ️  Дані вже існують у базі даних")
        except PyMongoError as e:
            print(f"❌ Помилка при створенні тестових даних: {e}")

    def read_all_cats(self):
        """Читання - виведення всіх записів із колекції"""
        try:
            cats = list(self.collection.find())
            if cats:
                print("\n📋 Всі коти в базі даних:")
                print("-" * 40)
                for cat in cats:
                    print(f"ID: {cat['_id']}")
                    print(f"Ім'я: {cat['name']}")
                    print(f"Вік: {cat['age']}")
                    print(f"Особливості: {', '.join(cat['features'])}")
                    print("-" * 40)
            else:
                print("📭 База даних порожня")
        except PyMongoError as e:
            print(f"❌ Помилка при читанні даних: {e}")

    def read_cat_by_name(self, name):
        """Читання - пошук кота за ім'ям"""
        try:
            cat = self.collection.find_one({"name": name})
            if cat:
                print(f"\n🐱 Знайдено кота:")
                print("-" * 40)
                print(f"ID: {cat['_id']}")
                print(f"Ім'я: {cat['name']}")
                print(f"Вік: {cat['age']}")
                print(f"Особливості: {', '.join(cat['features'])}")
                print("-" * 40)
            else:
                print(f"😿 Кота з ім'ям '{name}' не знайдено")
        except PyMongoError as e:
            print(f"❌ Помилка при пошуку кота: {e}")

    def update_cat_age(self, name, new_age):
        """Оновлення - змінити вік кота за ім'ям"""
        try:
            result = self.collection.update_one(
                {"name": name},
                {"$set": {"age": new_age}}
            )
            
            if result.matched_count > 0:
                print(f"✅ Вік кота '{name}' оновлено на {new_age}")
            else:
                print(f"😿 Кота з ім'ям '{name}' не знайдено")
        except PyMongoError as e:
            print(f"❌ Помилка при оновленні віку: {e}")

    def add_cat_feature(self, name, new_feature):
        """Оновлення - додати нову характеристику до списку features"""
        try:
            result = self.collection.update_one(
                {"name": name},
                {"$addToSet": {"features": new_feature}}  # $addToSet не додає дублікати
            )
            
            if result.matched_count > 0:
                if result.modified_count > 0:
                    print(f"✅ Додано нову характеристику '{new_feature}' для кота '{name}'")
                else:
                    print(f"ℹ️  Характеристика '{new_feature}' вже існує у кота '{name}'")
            else:
                print(f"😿 Кота з ім'ям '{name}' не знайдено")
        except PyMongoError as e:
            print(f"❌ Помилка при додаванні характеристики: {e}")

    def delete_cat_by_name(self, name):
        """Видалення - видалити кота за ім'ям"""
        try:
            result = self.collection.delete_one({"name": name})
            
            if result.deleted_count > 0:
                print(f"✅ Кота '{name}' успішно видалено з бази даних")
            else:
                print(f"😿 Кота з ім'ям '{name}' не знайдено")
        except PyMongoError as e:
            print(f"❌ Помилка при видаленні кота: {e}")

    def delete_all_cats(self):
        """Видалення - видалити всі записи з колекції"""
        try:
            # Підтвердження від користувача
            confirmation = input("⚠️  Ви впевнені, що хочете видалити всіх котів? (yes/no): ").lower()
            
            if confirmation in ['yes', 'y', 'так', 'т']:
                result = self.collection.delete_many({})
                print(f"✅ Видалено {result.deleted_count} котів з бази даних")
            else:
                print("❌ Операцію скасовано")
        except PyMongoError as e:
            print(f"❌ Помилка при видаленні всіх котів: {e}")

    def add_new_cat(self, name, age, features):
        """Створення - додати нового кота"""
        try:
            # Перевіряємо, чи не існує вже кота з таким ім'ям
            existing_cat = self.collection.find_one({"name": name})
            if existing_cat:
                print(f"⚠️  Кіт з ім'ям '{name}' вже існує в базі даних")
                return
            
            new_cat = {
                "name": name,
                "age": age,
                "features": features
            }
            
            result = self.collection.insert_one(new_cat)
            print(f"✅ Новий кіт '{name}' доданий до бази даних з ID: {result.inserted_id}")
        except PyMongoError as e:
            print(f"❌ Помилка при додаванні нового кота: {e}")

    def close_connection(self):
        """Закриває підключення до MongoDB"""
        try:
            self.client.close()
            print("🔌 Підключення до MongoDB закрито")
        except Exception as e:
            print(f"❌ Помилка при закритті підключення: {e}")

def display_menu():
    """Відображає меню програми"""
    print("\n" + "="*50)
    print("🐱 СИСТЕМА УПРАВЛІННЯ КОТАМИ - MONGODB")
    print("="*50)
    print("1. 📋 Показати всіх котів")
    print("2. 🔍 Знайти кота за ім'ям")
    print("3. 🎂 Оновити вік кота")
    print("4. ➕ Додати характеристику коту")
    print("5. ➕ Додати нового кота")
    print("6. ❌ Видалити кота за ім'ям")
    print("7. 💣 Видалити всіх котів")
    print("8. 🚪 Вийти")
    print("="*50)

def get_user_input(prompt, input_type=str):
    """Отримує та валідує введення користувача"""
    while True:
        try:
            value = input_type(input(prompt))
            return value
        except ValueError:
            print(f"❌ Помилка: введіть коректне значення типу {input_type.__name__}")

def main():
    """Основна функція програми"""
    print("🚀 Запуск програми управління котами...")
    
    # Ініціалізуємо базу даних
    cats_db = CatsDatabase()
    
    # Створюємо тестові дані
    cats_db.create_sample_data()
    
    try:
        while True:
            display_menu()
            choice = get_user_input("Оберіть опцію (1-8): ")
            
            if choice == "1":
                cats_db.read_all_cats()
                
            elif choice == "2":
                name = get_user_input("Введіть ім'я кота: ").strip()
                if name:
                    cats_db.read_cat_by_name(name)
                else:
                    print("❌ Ім'я не може бути порожнім")
                    
            elif choice == "3":
                name = get_user_input("Введіть ім'я кота: ").strip()
                if name:
                    age = get_user_input("Введіть новий вік: ", int)
                    if age >= 0:
                        cats_db.update_cat_age(name, age)
                    else:
                        print("❌ Вік не може бути від'ємним")
                else:
                    print("❌ Ім'я не може бути порожнім")
                    
            elif choice == "4":
                name = get_user_input("Введіть ім'я кота: ").strip()
                if name:
                    feature = get_user_input("Введіть нову характеристику: ").strip()
                    if feature:
                        cats_db.add_cat_feature(name, feature)
                    else:
                        print("❌ Характеристика не може бути порожньою")
                else:
                    print("❌ Ім'я не може бути порожнім")
                    
            elif choice == "5":
                name = get_user_input("Введіть ім'я нового кота: ").strip()
                if name:
                    age = get_user_input("Введіть вік: ", int)
                    if age >= 0:
                        print("Введіть характеристики кота (через кому):")
                        features_input = get_user_input("Характеристики: ").strip()
                        features = [f.strip() for f in features_input.split(",") if f.strip()]
                        if features:
                            cats_db.add_new_cat(name, age, features)
                        else:
                            print("❌ Додайте принаймні одну характеристику")
                    else:
                        print("❌ Вік не може бути від'ємним")
                else:
                    print("❌ Ім'я не може бути порожнім")
                    
            elif choice == "6":
                name = get_user_input("Введіть ім'я кота для видалення: ").strip()
                if name:
                    cats_db.delete_cat_by_name(name)
                else:
                    print("❌ Ім'я не може бути порожнім")
                    
            elif choice == "7":
                cats_db.delete_all_cats()
                
            elif choice == "8":
                print("👋 До побачення!")
                break
                
            else:
                print("❌ Невірний вибір. Оберіть число від 1 до 8")
                
            # Пауза перед наступною ітерацією
            input("\nНатисніть Enter для продовження...")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Програма перервана користувачем")
    except Exception as e:
        print(f"\n❌ Непередбачена помилка: {e}")
    finally:
        cats_db.close_connection()

if __name__ == "__main__":
    main()
