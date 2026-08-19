import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row
    
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        tasks.*,
        groups.name
    FROM tasks
    LEFT JOIN groups
        ON tasks.group_id = groups.id
    """)

    tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        name="Taskmanager",
        tasks=tasks
    )