from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import datetime

app = FastAPI()

# Allow CORS from your frontend IP or wildcard (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://192.168.1.15:19000"] for Expo default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for a log entry
class LogEntry(BaseModel):
    timestamp: str
    payout: str

# Dummy sniper logs data (replace with your DB or OCR output)
logs: List[LogEntry] = [
    {"timestamp": "20250730_101500", "payout": "Won $12.50"},
    {"timestamp": "20250730_101510", "payout": "Won $0.75"},
    {"timestamp": "20250730_101520", "payout": "Won $5.00"},
]

@app.get("/logs", response_model=List[LogEntry])
async def get_logs():
    # In reality, fetch from DB or OCR process here
    # Return latest logs (reverse chronological)
    return logs[::-1]

