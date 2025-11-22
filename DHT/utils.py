import urllib

import requests
from django.conf import settings

def send_telegram(text: str) -> bool:
    """Envoie un message Telegram via l'API officielle. Retourne True si OK."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot8544825366:AAFYS-dSIFcirgJ7WOiNYnzTk-7A0moZ8CQ/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": text})
        return r.ok
    except Exception:
        return False


def send_whatsapp_alert(phone_number: str, message: str):
    encoded_message = urllib.parse.quote(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={encoded_message}&apikey={settings.CALLMEBOT_APIKEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"✅ WhatsApp alert sent to {phone_number}")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp alert to {phone_number}: {e}")