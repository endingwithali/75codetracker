import sqlite3
import datetime

connection = sqlite3.connect('database.db')

current_date = datetime.datetime.now().date()


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks (user_id, day, task1, task2, task3, task4, task5) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('tester1', current_date, 'FALSE',  'FALSE',  'FALSE',  'FALSE',  'FALSE')
            )

connection.commit()
connection.close()