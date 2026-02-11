import os
import json
import redis
import requests

from config import *

# =========================
# Redis init
# =========================
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=REDIS_SSL,
    decode_responses=True
)

# =========================
# Settings
# =========================
REDIS_KEY = f"file:{REMOTE_PATH}"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# =========================
# Get data from Redis
# =========================
data = r.get(REDIS_KEY)

if not data:
    print("❌ Redisda data topilmadi yoki TTL tugagan")
    exit()

data = json.loads(data)

signed_url = data.get("signed_url")

if not signed_url:
    print("❌ Signed URL yo‘q")
    exit()

print("⬇️ Downloading via signed URL...")

# =========================
# Download file
# =========================
response = requests.get(signed_url, stream=True)

if response.status_code != 200:
    print("❌ Download failed:", response.status_code)
    exit()

# Fayl nomini URL’dan ajratamiz
filename = REDIS_KEY.split("/")[-1]
local_path = os.path.join(DOWNLOAD_DIR, filename)

with open(local_path, "wb") as f:
    for chunk in response.iter_content(8192):
        f.write(chunk)

print("✅ Downloaded:", local_path)
