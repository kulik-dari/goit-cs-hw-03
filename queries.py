import pg8000

DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'database': 'task_management',
    'user': 'dashakulikova',
    'port': 5432
}

def execute_query(query, params=None, fetch=True):
    """Виконує SQL запит та повертає результат"""
    try:
        conn = pg8000.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
            
        conn.commit()
        conn.close()
        return result
        
    except Exception as e:
        print(f"Помилка при виконанні запиту: {e}")
        return None

def query_1_get_user_tasks(user_id=1):
    """1. Отримати всі завдання певного користувача"""
    query = """
    SELECT t.id, t.title, t.description, s.name as status, u.fullname
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    JOIN status s ON t.status_id = s.id
    WHERE u.id = %s
    """
    print(f"1. Завдання користувача з ID {user_id}:")
    results = execute_query(query, [user_id])
    if results:
        for row in results:
            print(f"   ID: {row[0]}, Назва: {row[1]}, Статус: {row[3]}")
    else:
        print("   Завдання не знайдено")
    print()

def query_2_tasks_by_status(status_name='new'):
    """2. Вибрати завдання за певним статусом"""
    query = """
    SELECT t.id, t.title, t.description, u.fullname
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE t.status_id = (SELECT id FROM status WHERE name = %s)
    """
    print(f"2. Завдання зі статусом '{status_name}':")
    results = execute_query(query, [status_name])
    if results:
        for row in results:
            print(f"   ID: {row[0]}, Назва: {row[1]}, Користувач: {row[3]}")
    else:
        print("   Завдання не знайдено")
    print()

def query_3_update_task_status(task_id=1, new_status='in progress'):
    """3. Оновити статус конкретного завдання"""
    query = """
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = %s)
    WHERE id = %s
    """
    print(f"3. Оновлення статусу завдання ID {task_id} на '{new_status}':")
    result = execute_query(query, [new_status, task_id], fetch=False)
    if result and result > 0:
        print(f"   Статус оновлено для {result} завдання")
    else:
        print("   Завдання не знайдено або статус не змінено")
    print()

def query_4_users_without_tasks():
    """4. Отримати список користувачів, які не мають жодного завдання"""
    query = """
    SELECT u.id, u.fullname, u.email
    FROM users u
    WHERE u.id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL)
    """
    print("4. Користувачі без завдань:")
    results = execute_query(query)
    if results:
        for row in results:
            print(f"   ID: {row[0]}, Ім'я: {row[1]}, Email: {row[2]}")
    else:
        print("   Всі користувачі мають завдання")
    print()

def query_5_add_new_task(title='Тестове завдання', description='Опис завдання', user_id=1, status_name='new'):
    """5. Додати нове завдання для конкретного користувача"""
    query = """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
    """
    print(f"5. Додавання нового завдання '{title}' для користувача ID {user_id}:")
    result = execute_query(query, [title, description, status_name, user_id], fetch=False)
    if result and result > 0:
        print(f"   Завдання успішно додано")
    else:
        print("   Помилка при додаванні завдання")
    print()

def query_6_incomplete_tasks():
    """6. Отримати всі завдання, які ще не завершено"""
    query = """
    SELECT t.id, t.title, t.description, s.name as status, u.fullname
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    JOIN status s ON t.status_id = s.id
    WHERE s.name != 'completed'
    """
    print("6. Незавершені завдання:")
    results = execute_query(query)
    if results:
        for row in results[:5]:  # Показуємо перші 5
            print(f"   ID: {row[0]}, Назва: {row[1]}, Статус: {row[3]}, Користувач: {row[4]}")
        if len(results) > 5:
            print(f"   ... та ще {len(results) - 5} завдань")
    else:
        print("   Всі завдання завершено")
    print()

def query_7_delete_task(task_id=999):
    """7. Видалити конкретне завдання"""
    query = "DELETE FROM tasks WHERE id = %s"
    print(f"7. Видалення завдання ID {task_id}:")
    result = execute_query(query, [task_id], fetch=False)
    if result and result > 0:
        print(f"   Завдання успішно видалено")
    else:
        print("   Завдання не знайдено")
    print()

def query_8_find_users_by_email(email_pattern='gmail'):
    """8. Знайти користувачів з певною електронною поштою"""
    query = """
    SELECT id, fullname, email
    FROM users
    WHERE email LIKE %s
    """
    print(f"8. Користувачі з email що містить '{email_pattern}':")
    results = execute_query(query, [f'%{email_pattern}%'])
    if results:
        for row in results:
            print(f"   ID: {row[0]}, Ім'я: {row[1]}, Email: {row[2]}")
    else:
        print("   Користувачі не знайдені")
    print()

def query_9_update_user_name(user_id=1, new_name='Оновлений Користувач'):
    """9. Оновити ім'я користувача"""
    query = "UPDATE users SET fullname = %s WHERE id = %s"
    print(f"9. Оновлення імені користувача ID {user_id} на '{new_name}':")
    result = execute_query(query, [new_name, user_id], fetch=False)
    if result and result > 0:
        print(f"   Ім'я користувача успішно оновлено")
    else:
        print("   Користувача не знайдено")
    print()

def query_10_count_tasks_by_status():
    """10. Отримати кількість завдань для кожного статусу"""
    query = """
    SELECT s.name, COUNT(t.id) as task_count
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.id, s.name
    ORDER BY task_count DESC
    """
    print("10. Кількість завдань за статусами:")
    results = execute_query(query)
    if results:
        for row in results:
            print(f"   {row[0]}: {row[1]} завдань")
    else:
        print("   Немає даних")
    print()

def query_11_tasks_by_email_domain(domain='@gmail.com'):
    """11. Отримати завдання користувачів з певним доменом електронної пошти"""
    query = """
    SELECT t.id, t.title, u.fullname, u.email, s.name as status
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    JOIN status s ON t.status_id = s.id
    WHERE u.email LIKE %s
    """
    print(f"11. Завдання користувачів з доменом '{domain}':")
    results = execute_query(query, [f'%{domain}%'])
    if results:
        for row in results[:3]:  # Показуємо перші 3
            print(f"   ID: {row[0]}, Назва: {row[1]}, Користувач: {row[2]}")
        if len(results) > 3:
            print(f"   ... та ще {len(results) - 3} завдань")
    else:
        print("   Завдання не знайдено")
    print()

def query_12_tasks_without_description():
    """12. Отримати список завдань, що не мають опису"""
    query = """
    SELECT t.id, t.title, u.fullname, s.name as status
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    JOIN status s ON t.status_id = s.id
    WHERE t.description IS NULL OR t.description = ''
    """
    print("12. Завдання без опису:")
    results = execute_query(query)
    if results:
        for row in results:
            print(f"   ID: {row[0]}, Назва: {row[1]}, Користувач: {row[2]}, Статус: {row[3]}")
    else:
        print("   Всі завдання мають опис")
    print()

def query_13_users_with_in_progress_tasks():
    """13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'"""
    query = """
    SELECT u.id, u.fullname, u.email, t.id as task_id, t.title, t.description
    FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    INNER JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress'
    """
    print("13. Користувачі та їхні завдання в статусі 'in progress':")
    results = execute_query(query)
    if results:
        for row in results:
            print(f"   Користувач: {row[1]} (ID: {row[0]})")
            print(f"   Завдання: {row[4]} (ID: {row[3]})")
            print()
    else:
        print("   Немає завдань в статусі 'in progress'")
    print()

def query_14_users_with_task_count():
    """14. Отримати користувачів та кількість їхніх завдань"""
    query = """
    SELECT u.id, u.fullname, u.email, COUNT(t.id) as task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id, u.fullname, u.email
    ORDER BY task_count DESC
    """
    print("14. Користувачі та кількість їхніх завдань:")
    results = execute_query(query)
    if results:
        for row in results:
            print(f"   {row[1]} (ID: {row[0]}): {row[3]} завдань")
    else:
        print("   Немає даних")
    print()

def main():
    """Основна функція для виконання всіх запитів"""
    print("=" * 60)
    print("ВИКОНАННЯ SQL ЗАПИТІВ")
    print("=" * 60)
    
    # Виконуємо всі запити
    query_1_get_user_tasks(1)
    query_2_tasks_by_status('new')
    query_3_update_task_status(1, 'in progress')
    query_4_users_without_tasks()
    query_5_add_new_task('Нове тестове завдання', 'Опис нового завдання', 1)
    query_6_incomplete_tasks()
    query_7_delete_task(999)  # Неіснуючий ID
    query_8_find_users_by_email('gmail')
    query_9_update_user_name(1, 'Оновлений Користувач')
    query_10_count_tasks_by_status()
    query_11_tasks_by_email_domain('@gmail.com')
    query_12_tasks_without_description()
    query_13_users_with_in_progress_tasks()
    query_14_users_with_task_count()
    
    print("=" * 60)
    print("ВСІ ЗАПИТИ ВИКОНАНО")
    print("=" * 60)

if __name__ == "__main__":
    main()
