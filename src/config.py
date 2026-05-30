from typing import List
import os


def get_bot_token() -> str:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is required")
    return token


def get_allowed_usernames() -> List[str]:
    usernames = os.environ.get("ALLOWED_USERNAMES")
    if not usernames:
        raise ValueError("ALLOWED_USERNAMES environment variable is required")
    return [u.strip() for u in usernames.split(",")]



def get_allowed_user_ids() -> List[int]:
    user_id_str = os.environ.get("ALLOWED_USER_IDS")
    if not user_id_str:
        raise ValueError("ALLOWED_USER_IDS environment variable is required")
    try:
        return [int(uid.strip()) for uid in user_id_str.split(",")]
    except ValueError:
        raise ValueError("ALLOWED_USER_IDS must contain valid integers")


def get_rate_limit_max() -> int:
    try:
        return int(os.environ.get("RATE_LIMIT_MAX", "10"))
    except ValueError:
        return 10


def get_rate_limit_window() -> int:
    try:
        return int(os.environ.get("RATE_LIMIT_WINDOW", "60"))
    except ValueError:
        return 60
