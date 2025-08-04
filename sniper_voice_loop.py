import os, time, sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
from PIL import Image
import pytesseract
from vosk import Model, KaldiRecognizer
import wave
import json

app = Flask(__name__)
DB = "sniper_memory.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = Model("model/vosk-model-small-en-us-0.15")
def transcribe_voice(file_path):
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0: break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result += res.get("text", "") + " "
    return result.strip()

def extract_payout(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return next((line for line in text.splitlines() if "$" in line or "win" in line.lower()), "No win detected")
    except:
        return "OCR Failed"

def log_win(filename, result, origin="screenshot"):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS wins (id INTEGER PRIMARY KEY, file TEXT, result TEXT, origin TEXT, time TEXT)")
        conn.execute("INSERT INTO wins (file, result, origin, time) VALUES (?, ?, ?, ?)", (filename, result, origin, ts))

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok", "message": "Dardy Sniper v4.0 online"})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("screenshot")
    if not file:
        return jsonify({"error": "No file"}), 400
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + file.filename
    path = os.path.join(UPLOAD_DIR, filename)
    file.save(path)
    result = extract_payout(path)
    log_win(filename, result)
    return jsonify({"status": "scanned", "result": result})

@app.route("/voice", methods=["POST"])
def voice():
    file = request.files.get("file")
    if not file: return jsonify({"error": "No voice"}), 400
    fname = os.path.join("uploads", "input.wav")
    file.save(fname)
    text = transcribe_voice(fname)
    if "scan" in text or "sniper" in text:
        return jsonify({"status": "trigger", "message": "Scanning screenshot..."})
    return jsonify({"status": "voice", "heard": text})

@app.route("/log", methods=["GET"])
def log():
    with sqlite3.connect(DB) as conn:
        rows = conn.execute("SELECT * FROM wins ORDER BY id DESC LIMIT 25").fetchall()
    return jsonify([{"id": r[0], "file": r[1], "result": r[2], "origin": r[3], "time": r[4]} for r in rows])

if __name__ == "__main__":
    app.run(port=9124, host="0.0.0.0")
