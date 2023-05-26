import sqlite3
import random

connection = sqlite3.connect('news.db')
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM news")
row_count = cursor.fetchone()[0]

for i in range(row_count):
    random_value = random.choices(['good', 'maybe', 'never'], [0.3, 0.5, 0.2], k=1)[0]
    cursor.execute("UPDATE news SET label = ? WHERE id = ?", (random_value, i))
    connection.commit()

connection.close()
