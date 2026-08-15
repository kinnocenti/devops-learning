import sqlite3

connection = sqlite3.connect("taskmanager.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM tasks")

tasks = cursor.fetchall()

print(tasks)

connection.close()