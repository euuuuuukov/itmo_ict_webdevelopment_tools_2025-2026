# Лабораторная работа 2. Потоки. Процессы. Асинхронность.

## Задание 1

| threads                | processes            | async                  |
|------------------------|----------------------|------------------------|
| 0.003568887710571289 s | 2.0592732429504395 s | 0.010939836502075195 s |

Расчеты в отдельных задачах во всех программах реализованы по формуле суммы арифметической прогрессии, т.е. без циклов. Здесь потоки выигрывают, потому что они создаются очень быстро, расчет в одном потоке тоже выполняется очень быстро. Затем идет асинхронность, она в `gather` запускает все корутины последовательно. Здесь проиграли процессы, потому что на винде создание процессов очень затратно (каждый новый процесс запускает интерпретатор, загружает модули и т.п.)

## Задание 2

| threads            | processes           | async               |
|--------------------|---------------------|---------------------|
| 8.19732141494751 s | 18.33564853668213 s | 2.539149522781372 s |

<details>

<summary>Вывод для потоков</summary>

```
2026-05-12 19:49:07,494 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-05-12 19:49:07,495 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 19:49:07,511 INFO sqlalchemy.engine.Engine select current_schema()
2026-05-12 19:49:07,511 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 19:49:07,571 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2026-05-12 19:49:07,603 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 19:49:07,700 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:07,882 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:07,883 INFO sqlalchemy.engine.Engine [generated in 0.00069s] {}
2026-05-12 19:49:07,884 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:07,885 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:07,885 INFO sqlalchemy.engine.Engine [cached since 0.003094s ago] {}
2026-05-12 19:49:07,902 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:07,902 INFO sqlalchemy.engine.Engine [generated in 0.00093s] {'title': 'Публикации / Моя лента / Хабр', 'description': 'https://habr.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 7, 896991), 'owner_id': 1}
2026-05-12 19:49:07,973 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:07,977 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:07,985 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:07,985 INFO sqlalchemy.engine.Engine [generated in 0.00037s] {'pk_1': 19}
2026-05-12 19:49:07,998 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:07,998 INFO sqlalchemy.engine.Engine [generated in 0.00042s] {'name_1': 'web parsing'}
2026-05-12 19:49:08,015 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:08,016 INFO sqlalchemy.engine.Engine [generated in 0.00039s] {'task_id': 19, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 10942), 'notes': None}
2026-05-12 19:49:08,021 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,024 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,026 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,026 INFO sqlalchemy.engine.Engine [generated in 0.00027s] {'pk_1': 19}
task_id 19: https://habr.com/ - Публикации / Моя лента / Хабр
2026-05-12 19:49:08,028 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:08,036 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:08,036 INFO sqlalchemy.engine.Engine [cached since 0.1353s ago] {'title': 'Welcome to Python.org', 'description': 'https://www.python.org/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 35232), 'owner_id': 1}
2026-05-12 19:49:08,040 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,044 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,044 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,044 INFO sqlalchemy.engine.Engine [cached since 0.05975s ago] {'pk_1': 20}
2026-05-12 19:49:08,046 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:08,047 INFO sqlalchemy.engine.Engine [cached since 0.04891s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:08,049 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:08,050 INFO sqlalchemy.engine.Engine [cached since 0.03435s ago] {'task_id': 20, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 49147), 'notes': None}
2026-05-12 19:49:08,051 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,052 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,053 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,053 INFO sqlalchemy.engine.Engine [cached since 0.02722s ago] {'pk_1': 20}
task_id 20: https://www.python.org/ - Welcome to Python.org
2026-05-12 19:49:08,055 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:08,122 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,123 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:08,123 INFO sqlalchemy.engine.Engine [cached since 0.2409s ago] {}
2026-05-12 19:49:08,129 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:08,129 INFO sqlalchemy.engine.Engine [cached since 0.2283s ago] {'title': 'Newest Questions - Stack Overflow', 'description': 'https://stackoverflow.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 128516), 'owner_id': 1}
2026-05-12 19:49:08,133 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,136 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,136 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,136 INFO sqlalchemy.engine.Engine [cached since 0.1518s ago] {'pk_1': 21}
2026-05-12 19:49:08,138 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:08,138 INFO sqlalchemy.engine.Engine [cached since 0.1403s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:08,140 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:08,140 INFO sqlalchemy.engine.Engine [cached since 0.1248s ago] {'task_id': 21, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 139654), 'notes': None}
2026-05-12 19:49:08,141 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,143 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,143 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,143 INFO sqlalchemy.engine.Engine [cached since 0.1175s ago] {'pk_1': 21}
task_id 21: https://stackoverflow.com/ - Newest Questions - Stack Overflow
2026-05-12 19:49:08,144 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:08,769 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,769 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:08,769 INFO sqlalchemy.engine.Engine [cached since 0.8874s ago] {}
2026-05-12 19:49:08,772 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:08,772 INFO sqlalchemy.engine.Engine [cached since 0.8713s ago] {'title': 'Hacker News', 'description': 'https://news.ycombinator.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 771528), 'owner_id': 1}
2026-05-12 19:49:08,773 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,775 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,775 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,775 INFO sqlalchemy.engine.Engine [cached since 0.7906s ago] {'pk_1': 22}
2026-05-12 19:49:08,777 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:08,777 INFO sqlalchemy.engine.Engine [cached since 0.7789s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:08,779 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:08,779 INFO sqlalchemy.engine.Engine [cached since 0.7637s ago] {'task_id': 22, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 8, 778442), 'notes': None}
2026-05-12 19:49:08,781 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:08,782 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:08,782 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:08,782 INFO sqlalchemy.engine.Engine [cached since 0.7567s ago] {'pk_1': 22}
task_id 22: https://news.ycombinator.com/ - Hacker News
2026-05-12 19:49:08,783 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:10,152 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,152 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:10,153 INFO sqlalchemy.engine.Engine [cached since 2.271s ago] {}
2026-05-12 19:49:10,155 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:10,155 INFO sqlalchemy.engine.Engine [cached since 2.254s ago] {'title': 'no title', 'description': 'https://www.wikipedia.org/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 10, 154511), 'owner_id': 1}
2026-05-12 19:49:10,156 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:10,160 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,160 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:10,160 INFO sqlalchemy.engine.Engine [cached since 2.176s ago] {'pk_1': 23}
2026-05-12 19:49:10,162 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:10,162 INFO sqlalchemy.engine.Engine [cached since 2.164s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:10,164 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:10,164 INFO sqlalchemy.engine.Engine [cached since 2.149s ago] {'task_id': 23, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 10, 163884), 'notes': None}
2026-05-12 19:49:10,165 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:10,167 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,167 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:10,167 INFO sqlalchemy.engine.Engine [cached since 2.141s ago] {'pk_1': 23}
task_id 23: https://www.wikipedia.org/ - no title
2026-05-12 19:49:10,168 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:10,252 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,252 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:10,253 INFO sqlalchemy.engine.Engine [cached since 2.371s ago] {}
2026-05-12 19:49:10,255 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:10,255 INFO sqlalchemy.engine.Engine [cached since 2.354s ago] {'title': 'no title', 'description': 'https://www.yahoo.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 10, 254554), 'owner_id': 1}
2026-05-12 19:49:10,257 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:10,258 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,258 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:10,258 INFO sqlalchemy.engine.Engine [cached since 2.274s ago] {'pk_1': 24}
2026-05-12 19:49:10,260 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:10,260 INFO sqlalchemy.engine.Engine [cached since 2.263s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:10,262 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:10,262 INFO sqlalchemy.engine.Engine [cached since 2.247s ago] {'task_id': 24, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 10, 262102), 'notes': None}
2026-05-12 19:49:10,264 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:10,265 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,266 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:10,266 INFO sqlalchemy.engine.Engine [cached since 2.24s ago] {'pk_1': 24}
task_id 24: https://www.yahoo.com/ - no title
2026-05-12 19:49:10,267 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:10,578 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,578 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:10,578 INFO sqlalchemy.engine.Engine [cached since 2.696s ago] {}
2026-05-12 19:49:10,581 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:10,581 INFO sqlalchemy.engine.Engine [cached since 2.68s ago] {'title': 'Reddit - Please wait for verification', 'description': 'https://www.reddit.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 10, 580501), 'owner_id': 1}
2026-05-12 19:49:10,582 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:10,583 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,584 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:10,584 INFO sqlalchemy.engine.Engine [cached since 2.599s ago] {'pk_1': 25}
2026-05-12 19:49:10,585 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:10,586 INFO sqlalchemy.engine.Engine [cached since 2.588s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:10,587 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:10,588 INFO sqlalchemy.engine.Engine [cached since 2.572s ago] {'task_id': 25, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 10, 587310), 'notes': None}
2026-05-12 19:49:10,588 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:10,590 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:10,590 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:10,590 INFO sqlalchemy.engine.Engine [cached since 2.564s ago] {'pk_1': 25}
task_id 25: https://www.reddit.com/ - Reddit - Please wait for verification
2026-05-12 19:49:10,591 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 19:49:12,159 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:12,159 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 19:49:12,159 INFO sqlalchemy.engine.Engine [cached since 4.277s ago] {}
2026-05-12 19:49:12,162 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 19:49:12,162 INFO sqlalchemy.engine.Engine [cached since 4.261s ago] {'title': 'GitHub · Change is constant. GitHub keeps you ahead. · GitHub', 'description': 'https://www.github.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 16, 49, 12, 161401), 'owner_id': 1}
2026-05-12 19:49:12,164 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:12,165 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:12,165 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:12,165 INFO sqlalchemy.engine.Engine [cached since 4.181s ago] {'pk_1': 26}
2026-05-12 19:49:12,167 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 19:49:12,167 INFO sqlalchemy.engine.Engine [cached since 4.17s ago] {'name_1': 'web parsing'}
2026-05-12 19:49:12,169 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 19:49:12,169 INFO sqlalchemy.engine.Engine [cached since 4.154s ago] {'task_id': 26, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 16, 49, 12, 168951), 'notes': None}
2026-05-12 19:49:12,170 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 19:49:12,171 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 19:49:12,172 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 19:49:12,172 INFO sqlalchemy.engine.Engine [cached since 4.146s ago] {'pk_1': 26}
task_id 26: https://www.github.com/ - GitHub · Change is constant. GitHub keeps you ahead. · GitHub
2026-05-12 19:49:12,173 INFO sqlalchemy.engine.Engine ROLLBACK
threads: 8.19732141494751 s
```

</details>

<details>

<summary>Вывод для процессов</summary>

```
2026-05-12 20:03:35,921 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-05-12 20:03:35,922 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:35,926 INFO sqlalchemy.engine.Engine select current_schema()
2026-05-12 20:03:35,926 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:35,930 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2026-05-12 20:03:35,930 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:35,931 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:35,965 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:35,965 INFO sqlalchemy.engine.Engine [generated in 0.00032s] {}
2026-05-12 20:03:35,987 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:35,987 INFO sqlalchemy.engine.Engine [generated in 0.00125s] {'title': 'Welcome to Python.org', 'description': 'https://www.python.org/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 35, 982384), 'owner_id': 1}
2026-05-12 20:03:36,017 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:36,021 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:36,026 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:36,026 INFO sqlalchemy.engine.Engine [generated in 0.00033s] {'pk_1': 29}
2026-05-12 20:03:36,031 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:36,031 INFO sqlalchemy.engine.Engine [generated in 0.00031s] {'name_1': 'web parsing'}
2026-05-12 20:03:36,042 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:36,042 INFO sqlalchemy.engine.Engine [generated in 0.00034s] {'task_id': 29, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 36, 39909), 'notes': None}
2026-05-12 20:03:36,046 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:36,047 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:36,049 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:36,049 INFO sqlalchemy.engine.Engine [generated in 0.00021s] {'pk_1': 29}
task_id 29: https://www.python.org/ - Welcome to Python.org
2026-05-12 20:03:36,051 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:38,065 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-05-12 20:03:38,065 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:38,067 INFO sqlalchemy.engine.Engine select current_schema()
2026-05-12 20:03:38,067 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:38,068 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2026-05-12 20:03:38,068 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:38,068 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:38,103 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:38,103 INFO sqlalchemy.engine.Engine [generated in 0.00032s] {}
2026-05-12 20:03:38,113 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:38,113 INFO sqlalchemy.engine.Engine [generated in 0.00044s] {'title': 'GitHub · Change is constant. GitHub keeps you ahead. · GitHub', 'description': 'https://www.github.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 38, 108773), 'owner_id': 1}
2026-05-12 20:03:38,118 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:38,121 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:38,125 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:38,125 INFO sqlalchemy.engine.Engine [generated in 0.00026s] {'pk_1': 30}
2026-05-12 20:03:38,130 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:38,130 INFO sqlalchemy.engine.Engine [generated in 0.00029s] {'name_1': 'web parsing'}
2026-05-12 20:03:38,137 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:38,137 INFO sqlalchemy.engine.Engine [generated in 0.00031s] {'task_id': 30, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 38, 135518), 'notes': None}
2026-05-12 20:03:38,141 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:38,142 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:38,144 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:38,144 INFO sqlalchemy.engine.Engine [generated in 0.00019s] {'pk_1': 30}
task_id 30: https://www.github.com/ - GitHub · Change is constant. GitHub keeps you ahead. · GitHub
2026-05-12 20:03:38,146 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:39,496 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-05-12 20:03:39,496 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:39,497 INFO sqlalchemy.engine.Engine select current_schema()
2026-05-12 20:03:39,497 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:39,498 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2026-05-12 20:03:39,498 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:39,499 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:39,534 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:39,534 INFO sqlalchemy.engine.Engine [generated in 0.00036s] {}
2026-05-12 20:03:39,544 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:39,544 INFO sqlalchemy.engine.Engine [generated in 0.00045s] {'title': 'no title', 'description': 'https://www.wikipedia.org/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 39, 539670), 'owner_id': 1}
2026-05-12 20:03:39,548 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:39,551 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:39,555 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:39,555 INFO sqlalchemy.engine.Engine [generated in 0.00025s] {'pk_1': 31}
2026-05-12 20:03:39,560 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:39,560 INFO sqlalchemy.engine.Engine [generated in 0.00030s] {'name_1': 'web parsing'}
2026-05-12 20:03:39,567 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:39,567 INFO sqlalchemy.engine.Engine [generated in 0.00032s] {'task_id': 31, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 39, 565226), 'notes': None}
2026-05-12 20:03:39,571 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:39,572 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:39,574 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:39,574 INFO sqlalchemy.engine.Engine [generated in 0.00022s] {'pk_1': 31}
task_id 31: https://www.wikipedia.org/ - no title
2026-05-12 20:03:39,575 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:40,238 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-05-12 20:03:40,238 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:40,240 INFO sqlalchemy.engine.Engine select current_schema()
2026-05-12 20:03:40,240 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:40,241 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2026-05-12 20:03:40,241 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 20:03:40,242 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:40,275 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:40,275 INFO sqlalchemy.engine.Engine [generated in 0.00035s] {}
2026-05-12 20:03:40,285 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:40,285 INFO sqlalchemy.engine.Engine [generated in 0.00043s] {'title': 'Newest Questions - Stack Overflow', 'description': 'https://stackoverflow.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 40, 280931), 'owner_id': 1}
2026-05-12 20:03:40,289 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:40,292 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:40,297 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:40,297 INFO sqlalchemy.engine.Engine [generated in 0.00030s] {'pk_1': 32}
2026-05-12 20:03:40,302 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:40,303 INFO sqlalchemy.engine.Engine [generated in 0.00029s] {'name_1': 'web parsing'}
2026-05-12 20:03:40,309 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:40,310 INFO sqlalchemy.engine.Engine [generated in 0.00034s] {'task_id': 32, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 40, 307841), 'notes': None}
2026-05-12 20:03:40,313 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:40,314 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:40,316 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:40,316 INFO sqlalchemy.engine.Engine [generated in 0.00022s] {'pk_1': 32}
task_id 32: https://stackoverflow.com/ - Newest Questions - Stack Overflow
2026-05-12 20:03:40,318 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:43,868 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:43,869 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:43,870 INFO sqlalchemy.engine.Engine [cached since 5.767s ago] {}
2026-05-12 20:03:43,876 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:43,876 INFO sqlalchemy.engine.Engine [cached since 5.764s ago] {'title': 'Reddit - Please wait for verification', 'description': 'https://www.reddit.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 43, 873673), 'owner_id': 1}
2026-05-12 20:03:43,879 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:43,886 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:43,887 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:43,888 INFO sqlalchemy.engine.Engine [cached since 5.763s ago] {'pk_1': 33}
2026-05-12 20:03:43,891 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:43,892 INFO sqlalchemy.engine.Engine [cached since 5.762s ago] {'name_1': 'web parsing'}
2026-05-12 20:03:43,896 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:43,897 INFO sqlalchemy.engine.Engine [cached since 5.76s ago] {'task_id': 33, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 43, 894920), 'notes': None}
2026-05-12 20:03:43,900 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:43,902 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:43,904 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:43,904 INFO sqlalchemy.engine.Engine [cached since 5.76s ago] {'pk_1': 33}
task_id 33: https://www.reddit.com/ - Reddit - Please wait for verification
2026-05-12 20:03:43,907 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:44,151 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:44,151 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:44,152 INFO sqlalchemy.engine.Engine [cached since 8.187s ago] {}
2026-05-12 20:03:44,155 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:44,155 INFO sqlalchemy.engine.Engine [cached since 8.169s ago] {'title': 'Hacker News', 'description': 'https://news.ycombinator.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 44, 154278), 'owner_id': 1}
2026-05-12 20:03:44,157 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:44,161 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:44,162 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:44,162 INFO sqlalchemy.engine.Engine [cached since 8.137s ago] {'pk_1': 34}
2026-05-12 20:03:44,164 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:44,164 INFO sqlalchemy.engine.Engine [cached since 8.133s ago] {'name_1': 'web parsing'}
2026-05-12 20:03:44,166 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:44,166 INFO sqlalchemy.engine.Engine [cached since 8.124s ago] {'task_id': 34, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 44, 165861), 'notes': None}
2026-05-12 20:03:44,167 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:44,168 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:44,169 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:44,169 INFO sqlalchemy.engine.Engine [cached since 8.12s ago] {'pk_1': 34}
task_id 34: https://news.ycombinator.com/ - Hacker News
2026-05-12 20:03:44,170 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:45,511 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:45,512 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:45,512 INFO sqlalchemy.engine.Engine [cached since 5.237s ago] {}
2026-05-12 20:03:45,518 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:45,519 INFO sqlalchemy.engine.Engine [cached since 5.234s ago] {'title': 'no title', 'description': 'https://www.yahoo.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 45, 516420), 'owner_id': 1}
2026-05-12 20:03:45,527 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:45,531 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:45,532 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:45,532 INFO sqlalchemy.engine.Engine [cached since 5.235s ago] {'pk_1': 35}
2026-05-12 20:03:45,536 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:45,537 INFO sqlalchemy.engine.Engine [cached since 5.234s ago] {'name_1': 'web parsing'}
2026-05-12 20:03:45,541 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:45,542 INFO sqlalchemy.engine.Engine [cached since 5.232s ago] {'task_id': 35, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 45, 540216), 'notes': None}
2026-05-12 20:03:45,545 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:45,547 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:45,548 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:45,549 INFO sqlalchemy.engine.Engine [cached since 5.233s ago] {'pk_1': 35}
task_id 35: https://www.yahoo.com/ - no title
2026-05-12 20:03:45,551 INFO sqlalchemy.engine.Engine ROLLBACK
2026-05-12 20:03:46,593 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:46,594 INFO sqlalchemy.engine.Engine SELECT "user".id, "user".username, "user".email, "user".hashed_password, "user".is_active, "user".created_at 
FROM "user"
2026-05-12 20:03:46,594 INFO sqlalchemy.engine.Engine [cached since 7.06s ago] {}
2026-05-12 20:03:46,597 INFO sqlalchemy.engine.Engine INSERT INTO task (title, description, deadline, priority, status, estimated_hours, total_spent_hours, created_at, owner_id) VALUES (%(title)s, %(description)s, %(deadline)s, %(priority)s, %(status)s, %(estimated_hours)s, %(total_spent_hours)s, %(created_at)s, %(owner_id)s) RETURNING task.id
2026-05-12 20:03:46,597 INFO sqlalchemy.engine.Engine [cached since 7.053s ago] {'title': 'Публикации / Моя лента / Хабр', 'description': 'https://habr.com/', 'deadline': None, 'priority': 'MEDIUM', 'status': 'PENDING', 'estimated_hours': 0.0, 'total_spent_hours': 0.0, 'created_at': datetime.datetime(2026, 5, 12, 17, 3, 46, 596140), 'owner_id': 1}
2026-05-12 20:03:46,598 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:46,600 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:46,600 INFO sqlalchemy.engine.Engine SELECT task.id, task.title, task.description, task.deadline, task.priority, task.status, task.estimated_hours, task.total_spent_hours, task.created_at, task.owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:46,600 INFO sqlalchemy.engine.Engine [cached since 7.046s ago] {'pk_1': 36}
2026-05-12 20:03:46,602 INFO sqlalchemy.engine.Engine SELECT category.id, category.name, category.description 
FROM category 
WHERE category.name = %(name_1)s
2026-05-12 20:03:46,603 INFO sqlalchemy.engine.Engine [cached since 7.043s ago] {'name_1': 'web parsing'}
2026-05-12 20:03:46,605 INFO sqlalchemy.engine.Engine INSERT INTO taskcategorylink (task_id, category_id, assigned_at, notes) VALUES (%(task_id)s, %(category_id)s, %(assigned_at)s, %(notes)s)
2026-05-12 20:03:46,605 INFO sqlalchemy.engine.Engine [cached since 7.038s ago] {'task_id': 36, 'category_id': 2, 'assigned_at': datetime.datetime(2026, 5, 12, 17, 3, 46, 604490), 'notes': None}
2026-05-12 20:03:46,606 INFO sqlalchemy.engine.Engine COMMIT
2026-05-12 20:03:46,607 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 20:03:46,607 INFO sqlalchemy.engine.Engine SELECT task.id AS task_id, task.title AS task_title, task.description AS task_description, task.deadline AS task_deadline, task.priority AS task_priority, task.status AS task_status, task.estimated_hours AS task_estimated_hours, task.total_spent_hours AS task_total_spent_hours, task.created_at AS task_created_at, task.owner_id AS task_owner_id 
FROM task 
WHERE task.id = %(pk_1)s
2026-05-12 20:03:46,608 INFO sqlalchemy.engine.Engine [cached since 7.034s ago] {'pk_1': 36}
task_id 36: https://habr.com/ - Публикации / Моя лента / Хабр
2026-05-12 20:03:46,609 INFO sqlalchemy.engine.Engine ROLLBACK
threads: 18.33564853668213 s

Process finished with exit code 0
```

</details>

<details>

<summary>Вывод для асинхронности</summary>

```
task_id 58: https://www.python.org/ - Welcome to Python.org
task_id 59: https://stackoverflow.com/ - Just a moment...
task_id 60: https://www.yahoo.com/ - no title
task_id 61: https://www.reddit.com/ - Reddit - Please wait for verification
task_id 62: https://www.wikipedia.org/ - no title
task_id 63: https://habr.com/ - Публикации / Моя лента / Хабр
task_id 64: https://www.github.com/ - GitHub · Change is constant. GitHub keeps you ahead. · GitHub
task_id 65: https://news.ycombinator.com/ - Hacker News
```

</details>

Здесь видно, что самый быстрый способ - асинхронный, т.к. `asyncpg` создает пул соединений, который позволяет без лишних расходов работать с бд, поэтому она оптимальна (тут задача фактически i/o). Потоки медленнее примерно в 3-4 раза, потому что синхронные запросы в `requests` блокируют потоки. Самый медленный подход - процессы, потому что на винде создавать процессы очень дорого с точки зрения времени (повторюсь, каждый процесс запускает свой интерпретатор).