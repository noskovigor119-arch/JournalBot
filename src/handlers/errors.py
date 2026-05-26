import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update", exc_info=context.error)
    if update and hasattr(update, "effective_message"):
        await update.effective_message.reply_text("Something went wrong. Please try again later.")
