import sqlite3

conn = sqlite3.connect("prophecy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prophecies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# 🪄 Seed one sample prophecy so we can test immediately
cursor.execute(
    "INSERT INTO prophecies (message) VALUES (?)",
    ("When reels meet stars, fortune whispers truth.",)
)

conn.commit()
conn.close()

print("✅ prophecy.db initialized with table + sample entry.")
