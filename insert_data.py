import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    conn = sqlite3.connect('game_database.db')
    cursor = conn.cursor()

    # Extract data from the form
    # Use request.form.get('field_name') to get data from form fields

    # Insert data into the database
    cursor.execute('''
        INSERT INTO games (title, platform, ...)
        VALUES (?, ?, ...)
    ''', (title_value, platform_value, ...))

    conn.commit()
    conn.close()

    return "Game added successfully!"

if __name__ == '__main__':
    app.run()