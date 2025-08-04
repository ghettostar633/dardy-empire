import os
import pytesseract
from PIL import Image
import sqlite3
from datetime import datetime
import time

DB_FILE = 'sniper_memory.db'
SCREENSHOT_DIR = os.path.expanduser('~/screenshots')

def log_win(filename, amount):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sniper_wins
                 (id INTEGER PRIMARY KEY, filename TEXT, amount TEXT, timestamp TEXT)''')
    c.execute("INSERT INTO sniper_wins (filename, amount, timestamp) VALUES (?, ?, ?)",
              (filename, amount, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def detect_win(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        numbers = [s for s in text.split() if s.replace('.', '', 1).isdigit()]
        return numbers[0] if numbers else None
    except:
        return None

def run_loop():
    print("🔁 Starting Panomnia OCR Sniper Loop...")
    seen = set()
    while True:
        for file in os.listdir(SCREENSHOT_DIR):
            if file.endswith(('.png', '.jpg', '.jpeg')) and file not in seen:
                path = os.path.join(SCREENSHOT_DIR, file)
                amount = detect_win(path)
                if amount:
                    print(f"💰 WIN DETECTED: {amount} from {file}")
                    log_win(file, amount)
                    os.system("termux-media-player play /system/media/audio/ui/KeypressStandard.ogg")
                else:
                    print(f"❌ No win found in {file}")
                seen.add(file)
        time.sleep(5)

if __name__ == '__main__':
    run_loop()
