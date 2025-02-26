from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )''')
        conn.commit()

@app.route('/')
def home():
    today = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM journal WHERE date = ?", (today,))
        entry = cursor.fetchone()
        cursor.execute("SELECT DISTINCT strftime('%d', date) FROM journal WHERE strftime('%Y-%m', date) = ?", (today[:7],))
        entry_days = [int(day[0]) for day in cursor.fetchall()]
    if entry:
        entry = {"title": entry[1], "content": entry[2]}
    else:
        entry = {"title": "New Entry", "content": ""}
    return render_template('index.html', date=today, entry_title=entry["title"], entry_content=entry["content"], entry_days=entry_days)

@app.route('/save', methods=['POST'])
def save_entry():
    title = request.form['title']
    content = request.form['content']
    date = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO journal (title, content, date) VALUES (?, ?, ?)", (title, content, date))
        conn.commit()
    return redirect(url_for('home'))

@app.route('/entries')
def view_entries():
    today = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT strftime('%d', date) FROM journal WHERE strftime('%Y-%m', date) = ?", (today[:7],))
        entry_days = [int(day[0]) for day in cursor.fetchall()]
        cursor.execute("SELECT * FROM journal ORDER BY date DESC")
        entries = cursor.fetchall()
    return render_template('entries.html', entries=entries, entry_days=entry_days)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    today = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM journal WHERE id = ?", (entry_id,))
        entry = cursor.fetchone()
        cursor.execute("SELECT DISTINCT strftime('%d', date) FROM journal WHERE strftime('%Y-%m', date) = ?", (today[:7],))
        entry_days = [int(day[0]) for day in cursor.fetchall()]
    if entry:
        # Assuming your database returns (id, date, title, content)
        entry_data = {"id": entry[0], "date": entry[4], "title": entry[1], "content": entry[2]}
    else:
        entry_data = {}
    return render_template('entry.html', entry=entry_data, entry_days=entry_days)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)