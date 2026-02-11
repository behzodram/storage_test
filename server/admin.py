import firebase_admin
from firebase_admin import credentials, storage
from datetime import timedelta
from google.cloud.storage.blob import Blob

# 🔧 CONFIG
SERVICE_JSON = "serviceAccount.json"
BUCKET_NAME = "storage-test-d4789.firebasestorage.app"

LOCAL_FILE = "uploads/pol.jpg"
REMOTE_PATH = "uploads/pol.jpg"

# 🔐 Init Firebase
cred = credentials.Certificate(SERVICE_JSON)
firebase_admin.initialize_app(cred, {
    'storageBucket': BUCKET_NAME
})

bucket = storage.bucket()

# 📤 Upload
blob = bucket.blob(REMOTE_PATH)
blob.upload_from_filename(LOCAL_FILE)

print("✅ Upload bo‘ldi")

# 🌍 1️⃣ PUBLIC URL
public_url = blob.public_url
print("\n🌍 Public URL:")
print(public_url)


# ⏳ 2️⃣ SIGNED URL (Exp time)
signed_url = blob.generate_signed_url(
    expiration=timedelta(seconds=30),  # ⏰ 30 soniya amal qiladi
    method="GET"
)

print("\n⏳ Signed URL (1 soat amal qiladi):")
print(signed_url)
