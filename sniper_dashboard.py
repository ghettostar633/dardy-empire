from flask import Flask, request, render_template_string, redirect
import os, sqlite3, time
from datetime import datetime
from PIL import Image
import pytesseract

app = Flask(__name__)
DB_PATH = 'sniper_stats.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize SQLite
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    amount TEXT,
    timestamp TEXT
)''')
conn.commit()
conn.close()

# OCR Function
def detect_win_amount(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            if "$" in line or "win" in line.lower():
                return line
        return "No win detected"
    except Exception as e:
        return f"Error: {str(e)}"

# Routes
@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        file = request.files['screenshot']
        if file:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"{timestamp}_{file.filename}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            amount = detect_win_amount(save_path)

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO wins (filename, amount, timestamp) VALUES (?, ?, ?)", (filename, amount, timestamp))
            conn.commit()
            conn.close()

            return redirect("/")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename, amount, timestamp FROM wins ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()

    html = '''
    <html><head><title>🎯 Sniper Dashboard</title>
    <meta http-equiv="refresh" content="10" />
    </head><body style="background:#111;color:#0f0;font-family:sans-serif;">
    <h1>🔫 Dardy Sniper Dashboard</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="screenshot" accept="image/*" />
        <button type="submit">🔍 Upload & Scan</button>
    </form>
    <h2>🧠 Recent Detections</h2>
    <table border="1" style="color:#0f0;"><tr><th>File</th><th>Amount</th><th>Time</th></tr>
    {% for r in rows %}
    <tr><td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td></tr>
    {% endfor %}
    </table>
    </body></html>
    '''
    return render_template_string(html, rows=rows)

if __name__ == "__main__":
    app.run(port=9123, host="0.0.0.0")
