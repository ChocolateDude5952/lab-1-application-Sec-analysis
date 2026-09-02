import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret
SECRET_KEY = "super-secret-key-12345"

@app.route('/user')
def get_user():
    username = request.args.get('username')
    
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    
    return str(cursor.fetchone())

@app.route('/run-command')
def run_command():
    cmd = request.args.get('cmd')
    
    # VULNERABILITY 3: Command Injection
    # (Executing user input directly in the shell)
    os.system(cmd)
    return "Command executed"

if __name__ == "__main__":
    app.run()