import time, glob, os, requests

# ← point at your FastAPI upload endpoint on port 8000
API_URL = "http://127.0.0.1:8000/upload-scan/"
CASINO = "joker123"

while True:
    for img in glob.glob("screenshots/*.png"):
        with open(img, "rb") as f:
            try:
                # pass casino as query-param, file in multipart
                res = requests.post(f"{API_URL}?casino={CASINO}", files={"file": f})
                res.raise_for_status()
                print("✔️ Uploaded", img, "→", res.json())
                os.remove(img)
            except Exception as e:
                print("❌ Upload failed:", e)
    time.sleep(5)
