import sqlite3
import os
import subprocess
from flask import Flask, request, abort

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret
SECRET_KEY = "super-secret-key-12345"

ALLOWED_COMMANDS = {
    "list_files": ["ls"],
    "show_date": ["date"]
}

@app.route('/user')
def get_user():
    username = request.args.get('username')
    
    # VULNERABILITY 2: SQL Injection
    # (Using string formatting instead of parameterized queries)
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    
    return str(cursor.fetchone())

@app.route('/run-command')
def run_command():
    cmd = request.args.get('cmd')
    if cmd not in ALLOWED_COMMANDS:
        abort(400, description="Invalid command")

    subprocess.run(ALLOWED_COMMANDS[cmd], check=True)
    return "Command executed"

if __name__ == "__main__":
    app.run()