from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Taskmanager</title>
        </head>
        <body>
            <h1>Taskmanager</h1>
            <p>Willkommen bei unserem Taskmanager!</p>
        </body>
    </html>
    """