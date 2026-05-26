import os
import time
from collections import deque
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from src.config import get_allowed_username, get_allowed_user_id, get_rate_limit_max, get_rate_limit_window


_request_timestamps: deque = deque()


def _check_rate_limit() -> bool:
    now = time.time()
    max_requests = get_rate_limit_max()
    window = get_rate_limit_window()

    _request_timestamps.append(now)

    while _request_timestamps and _request_timestamps[0] <= now - window:
        _request_timestamps.popleft()

    if len(_request_timestamps) > max_requests:
        os._exit(1)
        return False

    return True

def _is_authorized(update: Update) -> bool:
    user = update.effective_user
    if not user:
        return False

    try:
        allowed_username = get_allowed_username()
        allowed_user_id = get_allowed_user_id()
    except ValueError:
        return False

    return user.username == allowed_username and user.id == allowed_user_id


async def security_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not _check_rate_limit():
        return False

    if not _is_authorized(update):
        if update.message:
            await update.message.reply_text("Unauthorized: Access denied.")
        return False

    return True


def with_security(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not _check_rate_limit():
            return None

        if not _is_authorized(update):
            if update.message:
                await update.message.reply_text("Unauthorized: Access denied.")
            return None

        return await func(update, context)

    return wrapper
