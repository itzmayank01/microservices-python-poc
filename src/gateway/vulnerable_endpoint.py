from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('users.db')

@app.route('/user')
def get_user():
    user_id = request.args.get('id')  # Step 1: tainted input from HTTP request
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM users WHERE id = " + user_id  # Step 2: tainted data concatenated
    
    cursor.execute(query)  # Step 3: tainted query reaches database sink
    
    result = cursor.fetchall()
    return str(result)

@app.route('/file')
def get_file():
    filename = request.args.get('name')  # tainted input
    
    with open('/var/data/' + filename, 'r') as f:  # path traversal vulnerability
        return f.read()

if __name__ == '__main__':
    app.run()
