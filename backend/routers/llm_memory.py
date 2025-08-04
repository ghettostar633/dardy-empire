from fastapi import APIRouter
import sqlite3
import requests
import json

router = APIRouter()

# Change to your real LLM endpoint if not using LM Studio or Ollama
LLM_API_URL = "http://localhost:11434/v1/chat/completions"

@router.get("/memory-response")
def memory_response():
    try:
        conn = sqlite3.connect("prophecy.db")
        cursor = conn.cursor()
        cursor.execute("SELECT message FROM prophecies ORDER BY id DESC LIMIT 10;")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"memory_response": "⚠️ No prophecies found in memory yet."}

        recent_logs = "\n".join([r[0] for r in rows])
        prompt = f"""
        You are an AI prophet that analyzes past casino sniper trends.
        These are the last few prophecies:
        {recent_logs}

        Based on this memory, what’s the next most likely trend to occur?
        Respond in a poetic prophetic tone.
        """

        payload = {
            "model": "mistral",
            "messages": [{"role": "user", "content": prompt}]
        }

        headers = {"Content-Type": "application/json"}
        res = requests.post(LLM_API_URL, headers=headers, data=json.dumps(payload))

        if res.status_code == 200:
            data = res.json()
            return {"memory_response": data["choices"][0]["message"]["content"]}
        else:
            return {"memory_response": "❌ Failed to fetch response", "details": res.text}

    except Exception as e:
        return {"memory_response": f"🔥 Internal error: {str(e)}"}
