from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import pytesseract
from PIL import Image
import io
import datetime

app = FastAPI()

# CORS config — open wide for development, lock down later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Swap with your frontend IP for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logs = []

class LogEntry(BaseModel):
    timestamp: str
    payout: str
    prophecy: str = ""
    filename: str = ""

@app.post("/scan", response_model=LogEntry)
async def scan_image(file: UploadFile = File(...)):
    content = await file.read()
    image = Image.open(io.BytesIO(content))

    text = pytesseract.image_to_string(image)
    print(f"\nOCR Dump:\n{text}\n")

    payout = "N/A"
    for line in text.splitlines():
        line_lower = line.lower()
        if "won" in line_lower:
            parts = line_lower.split("won")
            if len(parts) > 1:
                val = parts[1].strip().replace("$", "")
                try:
                    payout_val = float(val)
                    payout = f"Won ${payout_val:.2f}"
                    break
                except:
                    continue

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{timestamp}_{file.filename}"

    with open(filename, "wb") as f:
        f.write(content)

    prophecy = "Payout unclear. Game energy unstable..."

    entry = LogEntry(timestamp=timestamp, payout=payout, prophecy=prophecy, filename=filename)
    logs.append(entry)

    return entry

@app.get("/logs", response_model=List[LogEntry])
async def get_logs():
    return logs[::-1]

app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")
