import json
import time
import redis
import firebase_admin

from threading import Thread
from datetime import timedelta
from firebase_admin import credentials, storage

from config import *

# =========================
# Firebase Init
# =========================
cred = credentials.Certificate(SERVICE_JSON)
firebase_admin.initialize_app(cred, {
    "storageBucket": BUCKET_NAME
})

bucket = storage.bucket()

# =========================
# Redis Init
# =========================
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=REDIS_SSL,
    decode_responses=True
)

# =========================
# Upload function
# =========================
def upload_file():

    blob = bucket.blob(REMOTE_PATH)

    # Upload
    blob.upload_from_filename(LOCAL_FILE)

    # Public URL
    blob.make_public()
    public_url = blob.public_url

    # Signed URL
    signed_url = blob.generate_signed_url(
        expiration=timedelta(minutes=REDIS_VS_URL_TTL),
        method="GET"
    )

    print("Public:", public_url)
    print("Signed:", signed_url)

    # =========================
    # Redis SETEX (not queue)
    # =========================
    key = f"file:{blob.name}"

    data = {
        "public_url": public_url,
        "signed_url": signed_url
    }

    r.setex(
        key,
        REDIS_VS_URL_TTL * 60,
        json.dumps(data)
    )

    print(f"Redis setex done: {key} (TTL: {REDIS_VS_URL_TTL} min)")

    # =========================
    # Auto delete thread
    # =========================
    Thread(
        target=auto_delete,
        args=(blob.name,),
        daemon=True
    ).start()


# =========================
# Auto delete
# =========================
def auto_delete(blob_name):

    print(f"Delete timer started: {blob_name}")

    time.sleep(FIREBASE_DELETE_AFTER * 60)

    blob = bucket.blob(blob_name)
    blob.delete()

    print(f"Deleted from Firebase: {blob_name}")


# =========================
# Run
# =========================
if __name__ == "__main__":
    upload_file()
