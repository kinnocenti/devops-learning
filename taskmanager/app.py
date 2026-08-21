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
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name,

        GROUP_CONCAT(DISTINCT depends_on.title) AS depends_on_titles,
        GROUP_CONCAT(DISTINCT dependent.title) AS dependent_titles

    FROM tasks

    LEFT JOIN groups
        ON tasks.group_id = groups.id

    LEFT JOIN task_dependencies
        ON tasks.id = task_dependencies.task_id

    LEFT JOIN tasks AS depends_on
        ON task_dependencies.depends_on_task_id = depends_on.id

    LEFT JOIN task_dependencies AS reverse_dependencies
        ON tasks.id = reverse_dependencies.depends_on_task_id

    LEFT JOIN tasks AS dependent
        ON reverse_dependencies.task_id = dependent.id

    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name
    """)

    tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        name="Taskmanager",
        tasks=tasks
    )

@app.route("/task/<int:task_id>")
def task_detail(task_id):
    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name,

        GROUP_CONCAT(DISTINCT depends_on.title) AS depends_on_titles,
        GROUP_CONCAT(DISTINCT dependent.title) AS dependent_titles

    FROM tasks

    LEFT JOIN groups
        ON tasks.group_id = groups.id

    LEFT JOIN task_dependencies
        ON tasks.id = task_dependencies.task_id

    LEFT JOIN tasks AS depends_on
        ON task_dependencies.depends_on_task_id = depends_on.id

    LEFT JOIN task_dependencies AS reverse_dependencies
        ON tasks.id = reverse_dependencies.depends_on_task_id

    LEFT JOIN tasks AS dependent
        ON reverse_dependencies.task_id = dependent.id

    WHERE tasks.id = ?

    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name
    """, (task_id,))

    task = cursor.fetchone()

    connection.close()

    return render_template(
    "task.html",
    name="Aufgabe",
    task=task
)