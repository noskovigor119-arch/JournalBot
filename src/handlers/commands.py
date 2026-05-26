from telegram import Update
from telegram.ext import ContextTypes

from src.security import with_security
from src.clients.internal_api import get_status, plan_meal, plan_workout


@with_security
async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status = await get_status()
    await update.message.reply_text(status)


@with_security
async def handle_plan_meal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = " ".join(context.args) if context.args else "Standard default plan"
    result = await plan_meal(description)
    await update.message.reply_text(result)


@with_security
async def handle_plan_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = " ".join(context.args) if context.args else "Standard default plan"
    result = await plan_workout(description)
    await update.message.reply_text(result)
