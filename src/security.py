import os
import time
from collections import deque
from functools import wraps

import logging
from telegram import Update
from telegram.ext import ContextTypes

from src.config import get_allowed_usernames, get_allowed_user_ids, get_rate_limit_max, get_rate_limit_window


_request_timestamps: deque = deque()
logger = logging.getLogger(__name__)


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
        logger.warning("Unauthorized access attempt: No user found in update.")
        return False

    try:
        allowed_usernames = get_allowed_usernames()
        allowed_user_ids = get_allowed_user_ids()
    except ValueError as e:
        logger.error(f"Failed to retrieve security configuration: {e}")
        return False

    is_authorized = user.username in allowed_usernames and user.id in allowed_user_ids

    if not is_authorized:
        logger.warning(f"Unauthorized access attempt by user: {user.username} (ID: {user.id})")

    return is_authorized

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
