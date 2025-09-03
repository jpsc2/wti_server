# send_test_notification.py
import os
import sys
import django
from pyfcm import FCMNotification

# 1) Point to your Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecs.settings")

# 2) Make sure Python can import the project when run from this folder
sys.path.append(os.path.dirname(__file__))

# 3) Boot Django so we can read settings
django.setup()
from django.conf import settings  # noqa: E402

# ---- EDIT THIS: paste your device token below ----
DEVICE_TOKEN = "cR9Tf4mkS2S3tD2_halpHW:APA91bGh0zRjApUMadwZMmjCnnseJcCbxftTA5ql4vZ5YmCv0Lxt1I2FOY6wmW3WyU78WjFjdK0ST-b4zWGRwl5wBUnP2ykpuitnDpK36Ub6xvMaceOEM-o"
# --------------------------------------------------

def main():
    # Use Firebase Server Key from settings (make sure you added it in ecs/settings.py)
    server_key = getattr(settings, "FIREBASE_SERVER_KEY", None)
    if not server_key:
        raise RuntimeError("❌ FIREBASE_SERVER_KEY not found in settings.py. Please configure it.")

    push = FCMNotification(api_key=server_key)

    result = push.notify_single_device(
        registration_id=DEVICE_TOKEN,
        message_title="Test Notification",
        message_body="Hello from Django + FCM!"
    )

    print("✅ Notification result:", result)


if __name__ == "__main__":
    if DEVICE_TOKEN.startswith("PASTE_YOUR_DEVICE_TOKEN_HERE"):
        raise SystemExit("✋ Please paste your real device token into DEVICE_TOKEN first.")
    main()
