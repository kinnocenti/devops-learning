import sqlite3
from flask import Flask, render_template, request, redirect

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
        groups.name

    FROM tasks

    LEFT JOIN groups
        ON tasks.group_id = groups.id

    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name

    ORDER BY
        groups.name IS NULL,
        groups.name,
        tasks.title
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
        tasks.description,
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
        tasks.description,
        groups.name
    """, (task_id,))

    task = cursor.fetchone()

    connection.close()

    return render_template(
    "task.html",
    name="Aufgabe",
    task=task
)

@app.route("/create-group", methods=["GET", "POST"])
def create_group():

    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]

        cursor.execute(
            """
            INSERT INTO groups (name)
            VALUES (?)
            """,
            (name,)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    connection.close()

    return render_template(
        "create_group.html"
    )

@app.route("/create-task", methods=["GET", "POST"])
def create_task():
    
    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        deadline = request.form["deadline"]
        group_id = request.form["group_id"]

        if group_id == "":
            group_id = None

        cursor.execute(
            """
            INSERT INTO tasks (
                title,
                description,
                priority,
                status,
                deadline,
                group_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                priority,
                status,
                deadline,
                group_id
            )
        )

        connection.commit()
        connection.close()

        return redirect("/")

    cursor.execute(
        """
        SELECT id, name
        FROM groups
        ORDER BY name
        """
    )

    groups = cursor.fetchall()

    connection.close()

    return render_template(
        "create_task.html",
        groups=groups
    )