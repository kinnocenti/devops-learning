from flask import Flask, render_template

app = Flask(__name__)

tasks = [
    "Docker installieren",
    "Docker Tutorial Teil 1",
    "Docker Tutorial Teil 2",
    "Linuxbefehlsübersicht erstellen",
    "Docker Compose Grundlagen"
]

@app.route("/")

def home():
    return render_template(
        "index.html", 
        name="Taskmanager", 
        tasks=tasks
    )