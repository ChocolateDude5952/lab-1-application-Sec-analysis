import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret
SECRET_KEY = "super-secret-key-12345"

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
    
    # VULNERABILITY 3: Command Injection
    # (Executing user input directly in the shell)
    os.system(cmd)
    return "Command executed"

if __name__ == "__main__":
    app.run()