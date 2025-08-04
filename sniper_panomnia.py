from flask import Flask, request, render_template, jsonify
import os, sqlite3
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
DB_FILE = 'sniper_memory.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize SQLite DB
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS prophecies
             (id INTEGER PRIMARY KEY, message TEXT, timestamp TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Accept plain text file upload as prophecy
    file = request.files['file']
    text = file.read().decode('utf-8')
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.seek(0)
    file.save(filename)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO prophecies (message, timestamp) VALUES (?, ?)", 
              (text.strip(), datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "prophecy": text.strip()})

@app.route('/prophecies')
def get_prophecies():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM prophecies ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "message": r[1], "timestamp": r[2]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9124)

@app.route('/sniper-wins')
def sniper_wins():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sniper_wins (id INTEGER PRIMARY KEY, filename TEXT, amount TEXT, timestamp TEXT)")
    c.execute("SELECT * FROM sniper_wins ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "filename": r[1], "amount": r[2], "timestamp": r[3]} for r in rows
    ])

@app.route('/sniper-wins')
def sniper_wins():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sniper_wins (id INTEGER PRIMARY KEY, filename TEXT, amount TEXT, timestamp TEXT)")
    c.execute("SELECT * FROM sniper_wins ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "filename": r[1], "amount": r[2], "timestamp": r[3]} for r in rows
    ])
