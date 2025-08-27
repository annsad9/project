import sqlite3

conn = sqlite3.connect("data_123.db")

conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                order_date DATE NOT NULL)""")
conn.execute("""
                CREATE TABLE IF NOT EXISTS order_status_log (
                log_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)""")

# Вставка тестовых заказов
conn.execute("""
                INSERT INTO orders (order_id, customer_name, order_date) VALUES 
                (121, 'Иван Петров', '2024-03-01'))
                (122, 'Мария Сидорова', '2024-03-01'),
                (123, 'Алексей Иванов', '2024-03-01'),
                (124, 'Ольга Ветрова', '2024-03-02'),
                (125, 'Петр Николаев', '2024-03-02')
            """)

# Вставка данных в журнал статусов. Внимание на аномалии для заказа 123.
# Заказ 121: нормальный цикл
conn.execute("""
                INSERT INTO order_status_log (order_id, status, created_at) VALUES 
                (121, 'создан', '2024-03-01 10:00:00'),
                (121, 'в обработке', '2024-03-01 10:15:00'),
                (121, 'доставлен', '2024-03-01 15:30:00')
            """)
# Заказ 122: нормальный цикл
conn.execute("""
                INSERT INTO order_status_log (order_id, status, created_at) VALUES 
                (122, 'создан', '2024-03-01 11:30:00'),
                (122, 'в обработке', '2024-03-01 11:45:00'),
                (122, 'доставлен', '2024-03-02 12:00:00')
                """)

# Заказ 123: ПРОБЛЕМНЫЙ ЗАКАЗ с аномалией - возврат статуса
conn.execute("""
                INSERT INTO order_status_log (order_id, status, created_at) VALUES 
                (123, 'создан', '2024-03-01 09:00:00'),
                (123, 'в обработке', '2024-03-01 09:20:00'),
                (123, 'доставлен', '2024-03-01 14:00:00')
                """)
# Заказ доставлен...
conn.execute("""
                INSERT INTO order_status_log (order_id, status, created_at) VALUES 
                (123, 'в обработке', '2024-03-03 10:00:00')""")
# АНОМАЛИЯ: Возврат в "в обработке" после "доставлен"

# Заказ 124: нормальный цикл
conn.execute("""
                INSERT INTO order_status_log (order_id, status, created_at) VALUES 
                (124, 'создан', '2024-03-02 10:00:00'),
                (124, 'в обработке', '2024-03-02 10:10:00'),
                (124, 'доставлен', '2024-03-03 11:00:00')""")

# Заказ 125: нормальный цикл
conn.execute("""
                INSERT INTO order_status_log (order_id, status, created_at) VALUES 
                (125, 'создан', '2024-03-02 12:00:00'),
                (125, 'в обработке', '2024-03-02 12:20:00'),
                (125, 'доставлен', '2024-03-03 13:00:00')""")

conn.commit() #сохраняем изменения

cursor = conn.execute('SELECT * FROM orders')
for row in cursor:
    print(row)