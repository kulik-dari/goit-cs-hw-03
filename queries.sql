-- SQL запити для системи управління завданнями
-- База даних: task_management

-- 1. Отримати всі завдання певного користувача (user_id = 1)
SELECT t.id, t.title, t.description, s.name as status, u.fullname
FROM tasks t
JOIN users u ON t.user_id = u.id
JOIN status s ON t.status_id = s.id
WHERE u.id = 1;

-- 2. Вибрати завдання за певним статусом ('new')
SELECT t.id, t.title, t.description, u.fullname
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE t.status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання (task_id = 1 на 'in progress')
UPDATE tasks 
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT u.id, u.fullname, u.email
FROM users u
WHERE u.id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL);

-- 5. Додати нове завдання для конкретного користувача (user_id = 1)
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('Нове тестове завдання', 'Опис нового завдання', 
        (SELECT id FROM status WHERE name = 'new'), 1);

-- 6. Отримати всі завдання, які ще не завершено
SELECT t.id, t.title, t.description, s.name as status, u.fullname
FROM tasks t
JOIN users u ON t.user_id = u.id
JOIN status s ON t.status_id = s.id
WHERE s.name != 'completed';

-- 7. Видалити конкретне завдання (task_id = 5)
DELETE FROM tasks WHERE id = 5;

-- 8. Знайти користувачів з певною електронною поштою (містить 'gmail')
SELECT id, fullname, email
FROM users
WHERE email LIKE '%gmail%';

-- 9. Оновити ім'я користувача (user_id = 1)
UPDATE users 
SET fullname = 'Оновлене Ім''я Користувача'
WHERE id = 1;

-- 10. Отримати кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) as task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.id, s.name
ORDER BY task_count DESC;

-- 11. Отримати завдання користувачів з певним доменом email ('@gmail.com')
SELECT t.id, t.title, t.description, u.fullname, u.email, s.name as status
FROM tasks t
JOIN users u ON t.user_id = u.id
JOIN status s ON t.status_id = s.id
WHERE u.email LIKE '%@gmail.com%';

-- 12. Отримати список завдань, що не мають опису
SELECT t.id, t.title, u.fullname, s.name as status
FROM tasks t
JOIN users u ON t.user_id = u.id
JOIN status s ON t.status_id = s.id
WHERE t.description IS NULL OR t.description = '';

-- 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT u.id, u.fullname, u.email, t.id as task_id, t.title, t.description
FROM users u
INNER JOIN tasks t ON u.id = t.user_id
INNER JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT u.id, u.fullname, u.email, COUNT(t.id) as task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname, u.email
ORDER BY task_count DESC;
