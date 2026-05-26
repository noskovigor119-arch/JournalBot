import os


def get_bot_token() -> str:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is required")
    return token


def get_allowed_username() -> str:
    username = os.environ.get("ALLOWED_USERNAME")
    if not username:
        raise ValueError("ALLOWED_USERNAME environment variable is required")
    return username


def get_allowed_user_id() -> int:
    user_id_str = os.environ.get("ALLOWED_USER_ID")
    if not user_id_str:
        raise ValueError("ALLOWED_USER_ID environment variable is required")
    try:
        return int(user_id_str)
    except ValueError:
        raise ValueError("ALLOWED_USER_ID must be a valid integer")


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
