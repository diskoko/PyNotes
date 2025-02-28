from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    """
    Initialize the SQLite database with the journal table.
    Creates the table if it doesn't exist.
    """
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        # Create journal table with proper field order and added timestamp
        cursor.execute('''CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,           -- Entry title
            content TEXT NOT NULL,         -- Journal content
            date TEXT NOT NULL,            -- Date in YYYY-MM-DD format
            formatted_date TEXT GENERATED ALWAYS AS (
                strftime('%d %b %Y', date) -- Human-readable date format
            ) STORED,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- When entry was created
        )''')
        conn.commit()

@app.route('/')
def home():
    """
    Home page route - shows today's journal entry form or existing entry.
    Also displays a calendar highlighting days with entries.
    """
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Always start with empty entry
    entry = {
        "title": "", 
        "content": ""
    }
    
    # Connect to database and fetch calendar data
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        # Get list of days in current month that have journal entries
        current_month = today[:7]  # Extract YYYY-MM part
        cursor.execute("SELECT DISTINCT strftime('%d', date) FROM journal WHERE strftime('%Y-%m', date) = ?", 
                      (current_month,))
        # Convert day strings to integers for template rendering
        days_with_entries = [int(day[0]) for day in cursor.fetchall()]
    
    return render_template('index.html', 
                          date=today, 
                          entry_title=entry["title"], 
                          entry_content=entry["content"], 
                          entry_days=days_with_entries,
                          current_date=today)

@app.route('/save', methods=['POST'])
def save_entry():
    title = request.form['title']
    content = request.form['content']
    date = request.form['date']  # Get date from user input, not today's date

    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        try:
            # Attempt to insert a new entry with the user-selected date
            cursor.execute("INSERT INTO journal (title, content, date) VALUES (?, ?, ?)", 
                          (title, content, date))
            message = "New entry saved successfully."
        except sqlite3.IntegrityError:
            # Update entry if date already exists
            cursor.execute("UPDATE journal SET title = ?, content = ? WHERE date = ?", 
                          (title, content, date))
            message = "Entry updated successfully."
        conn.commit()

    return jsonify({
        'success': True,
        'title': title,
        'message': message
    })

@app.route('/entries')
def view_entries():
    """
    Show all journal entries, sorted by date (newest first).
    Also displays a calendar highlighting days with entries.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        # Get days with entries for current month
        current_month = today[:7]
        cursor.execute("SELECT DISTINCT strftime('%d', date) FROM journal WHERE strftime('%Y-%m', date) = ?", 
                      (current_month,))
        days_with_entries = [int(day[0]) for day in cursor.fetchall()]
        
        # Get all entries, newest first
        cursor.execute("SELECT id, title, content, date, strftime('%d-%m-%Y', date) as formatted_date FROM journal ORDER BY date DESC")
        all_entries = cursor.fetchall()
    
    # Generate days of current month for template
    days = range(1, 32)  # Maximum days in a month
    
    return render_template('entries.html', 
                          entries=all_entries, 
                          entry_days=days_with_entries,
                          days=days)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    """
    View a specific journal entry by its ID.
    Displays the entry and a calendar.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    with sqlite3.connect('journal.db') as conn:
        cursor = conn.cursor()
        # Get the specific entry
        cursor.execute("SELECT id, title, content, date FROM journal WHERE id = ?", (entry_id,))
        entry_data = cursor.fetchone()
        
        # Get days with entries for the calendar
        current_month = today[:7]
        cursor.execute("SELECT DISTINCT strftime('%d', date) FROM journal WHERE strftime('%Y-%m', date) = ?", 
                      (current_month,))
        days_with_entries = [int(day[0]) for day in cursor.fetchall()]
    
    # Format entry data for template if entry exists
    if entry_data:
        entry = {
            "id": entry_data[0], 
            "title": entry_data[1], 
            "content": entry_data[2],
            "date": entry_data[3]
        }
    else:
        # Handle case where entry doesn't exist
        entry = {"error": "Entry not found"}
    
    # Generate days of current month for template
    days = range(1, 32)
    
    return render_template('entry.html', 
                          entry=entry, 
                          entry_days=days_with_entries,
                          days=days)

if __name__ == '__main__':
    # Initialize database when app starts
    init_db()
    # Run Flask development server
    app.run(debug=True)