import

import pandas as pd

# Подключаемся к базе данных
conn = sqlite3.connect('data_123.db')

# 1. Получаем историю статусов для всех заказов
query = """
SELECT 
    order_id,
    status,
    created_at
FROM order_status_log
ORDER BY order_id, created_at ASC;
"""

df_log = pd.read_sql_query(query, conn)

# Преобразуем created_at в datetime с помощью pandas
df_log['created_at'] = pd.to_datetime(df_log['created_at'])

# 2. Вычисляем длительность каждого статуса для всех заказов
df_log['next_status_time'] = df_log.groupby('order_id')['created_at'].shift(-1)
df_log['duration_minutes'] = (df_log['next_status_time'] - df_log['created_at']).dt.total_seconds() / 60

# Убираем последний статус (у него нет следующего)
df_durations = df_log.dropna(subset=['duration_minutes'])

# 3. Вычисляем среднее время по каждому статусу
avg_durations = df_durations.groupby('status')['duration_minutes'].mean().reset_index()
avg_durations.columns = ['status', 'avg_duration_minutes']

# 4. Получаем данные для проблемного заказа 123
problem_order_durations = df_durations[df_durations['order_id'] == 123][['status', 'duration_minutes']]

# 5. Сравниваем с средними значениями
comparison = problem_order_durations.merge(avg_durations, on='status')
comparison['duration_vs_avg_percent'] = (
    (comparison['duration_minutes'] - comparison['avg_duration_minutes']) /
    comparison['avg_duration_minutes'] * 100
)

print("Сравнение времени в статусах заказа №123 со средними показателями:")
# вывод без индексов
print(comparison[['status', 'duration_minutes', 'avg_duration_minutes', 'duration_vs_avg_percent']].round(2).to_string(index=False))

# 6. Дополнительный анализ: выводим полную историю проблемного заказа
print("\nПолная история статусов заказа №123:")
problem_order_history = df_log[df_log['order_id'] == 123][['status', 'created_at', 'duration_minutes']]
# вывод без индексов
print(problem_order_history.to_string(index=False))

# Закрываем соединение с базой данных
conn.close()