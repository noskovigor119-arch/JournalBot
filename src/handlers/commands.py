from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown


from src.security import with_security
from src.clients.internal_api import get_status, plan_meal, plan_workout
from src.utils.formatter import format_for_telegram


@with_security
async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status = await get_status()
    await update.message.reply_text(status)


@with_security
async def handle_plan_meal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = " ".join(context.args) if context.args else "Standard default plan"
    user_id = str(update.effective_user.id)
    plan_response = await plan_meal(description, user_id)
    result = format_for_telegram(plan_response)
    await update.message.reply_html(result)


@with_security
async def handle_plan_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = " ".join(context.args) if context.args else "Standard default plan"
    plan_response = await plan_workout(description)
    result = format_for_telegram(plan_response)
    await update.message.reply_html(result)
