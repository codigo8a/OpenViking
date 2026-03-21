import os

def is_allowed(user_id: int) -> bool:
    """
    Checks if a Telegram user ID is in the whitelist.
    """
    allowed_ids_str = os.getenv("TELEGRAM_ALLOWED_USER_IDS", "")
    allowed_ids = [s.strip() for s in allowed_ids_str.split(",") if s.strip()]
    return str(user_id) in allowed_ids
