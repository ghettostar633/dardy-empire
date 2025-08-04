import os
import time
import sqlite3
import pytesseract
import datetime
import threading
from flask import Flask, jsonify, request, render_template_string
from PIL import Image, ImageEnhance, ImageFilter
import platform

# === CONFIG ===
SCAN_INTERVAL = 5
SCREENSHOT_PATH = "latest_screen.png"
DB = "sniper_mastermind.db"
PORT = 6969
CASINO_NAME = "default"

# === INIT DB ===
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS payouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    amount TEXT,
    casino TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS prophecies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    message TEXT
)''')
conn.commit()
conn.close()

# === OCR ===
def fuzzy_ocr(img_path):
    try:
        img = Image.open(img_path)
        img = img.convert('L').filter(ImageFilter.MedianFilter())
        img = ImageEnhance.Contrast(img).enhance(2)
        return pytesseract.image_to_string(img, config='--psm 6')
    except Exception as e:
        return f"OCR Error: {e}"

# === AI PROPHECY (Placeholder for local AI) ===
def generate_prophecy(amount):
    base = ["A great fortune has been revealed.", 
            "The slot gods speak again.", 
            "Jackpot winds stir in the code.", 
            "From coin to prophecy: a path of gold."]
    return f"{random.choice(base)} Win logged: {amount}"

def speak(message):
    try:
        if platform.system() == "Darwin":
            os.system(f"say '{message}'")
        else:
            os.system(f"termux-tts-speak '{message}'")
    except:
        pass

# === SNIPER LOOP ===
def sniper_loop():
    while True:
        print("🔍 Scanning...")
        os.system(f"screencap -p > {SCREENSHOT_PATH}")
        result = fuzzy_ocr(SCREENSHOT_PATH)
        print("🧠 OCR Result:", result)

        for line in result.splitlines():
            if "$" in line or "win" in line.lower():
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                amount = line.strip()

                # Log to DB
                conn = sqlite3.connect(DB)
                c = conn.cursor()
                c.execute("INSERT INTO payouts (timestamp, amount, casino) VALUES (?, ?, ?)",
                          (ts, amount, CASINO_NAME))
                conn.commit()

                # Generate prophecy
                prophecy = generate_prophecy(amount)
                c.execute("INSERT INTO prophecies (timestamp, message) VALUES (?, ?)", (ts, prophecy))
                conn.commit()
                conn.close()

                print(f"💰 WIN: {amount}")
                print(f"🔮 PROPHECY: {prophecy}")
                speak(prophecy)
        time.sleep(SCAN_INTERVAL)

# === DASHBOARD ===
app = Flask(__name__)
@app.route('/')
def dash():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT timestamp, amount FROM payouts ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    c.execute("SELECT timestamp, message FROM prophecies ORDER BY id DESC LIMIT 10")
    prophecies = c.fetchall()
    conn.close()
    return render_template_string('''
    <html>
    <head>
        <meta http-equiv="refresh" content="5">
        <title>🎯 Mastermind Sniper</title>
    </head>
    <body style="background:#000;color:#0f0;font-family:monospace">
        <h1>💸 Latest Wins</h1>
        {% for ts, amt in rows %}
            <div>{{ts}} → <b>{{amt}}</b></div>
        {% endfor %}
        <h2>🔮 Prophecies</h2>
        {% for ts, msg in prophecies %}
            <div>🕓 {{ts}} → {{msg}}</div>
        {% endfor %}
    </body>
    </html>
    ''', rows=rows, prophecies=prophecies)

@app.route('/scan-now', methods=['POST'])
def scan_now():
    os.system(f"screencap -p > {SCREENSHOT_PATH}")
    result = fuzzy_ocr(SCREENSHOT_PATH)
    return jsonify({"ocr": result})

# === LAUNCH ===
def launch():
    threading.Thread(target=sniper_loop, daemon=True).start()
    print(f"🧠 Sniper Mastermind started every {SCAN_INTERVAL}s")
    app.run(host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    import random
    launch()
