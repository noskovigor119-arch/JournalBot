import logging
import sys
import re

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from src.config import get_bot_token
from src.handlers.commands import handle_status, handle_plan_meal, handle_plan_workout, handle_calories
from src.handlers.errors import handle_error

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Regex breakdown:
# ^          : Start of the string
# calories   : The keyword
# \s* : Zero or more whitespace characters
# :          : The colon
# \s* : Optional trailing space before the user's text starts
calories_filter = filters.CaptionRegex(r'(?i)^calories\s*:\s*')

def main() -> None:
    application = ApplicationBuilder().token(get_bot_token()).build()

    application.add_handler(CommandHandler("status", handle_status))
    application.add_handler(CommandHandler("plan_meal", handle_plan_meal))
    application.add_handler(CommandHandler("plan_workout", handle_plan_workout))
    # This handler ONLY triggers if the message is a photo AND the caption is exactly "calories" (or starts with it)
    application.add_handler(MessageHandler(
        filters.PHOTO & calories_filter,
        handle_calories
    ))
    application.add_error_handler(handle_error)

    logger.info("Bot starting with long-polling...")
    application.run_polling()


if __name__ == "__main__":
    main()
