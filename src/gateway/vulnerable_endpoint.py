import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/users')
def get_users():
    username = request.args.get('username')  # source: user controlled input
    
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Taint flow: username flows directly into SQL query without sanitization
    cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")  # sink
    
    rows = cursor.fetchall()
    return str(rows)

@app.route('/files')  
def read_file():
    path = request.args.get('path')  # source: user controlled input
    
    # Taint flow: path flows directly into file open without sanitization
    with open(path, 'r') as f:  # sink: path traversal
        return f.read()


    
    
    
    
