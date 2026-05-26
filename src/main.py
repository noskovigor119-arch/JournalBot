import logging
import sys

from telegram.ext import ApplicationBuilder, CommandHandler

from src.config import get_bot_token
from src.handlers.commands import handle_status, handle_plan_meal, handle_plan_workout
from src.handlers.errors import handle_error
from src.security import with_security

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = ApplicationBuilder().token(get_bot_token()).build()

    application.add_handler(CommandHandler("status", with_security(handle_status)))
    application.add_handler(CommandHandler("plan_meal", with_security(handle_plan_meal)))
    application.add_handler(CommandHandler("plan_workout", with_security(handle_plan_workout)))
    application.add_error_handler(handle_error)

    logger.info("Bot starting with long-polling...")
    application.run_polling()


if __name__ == "__main__":
    main()
