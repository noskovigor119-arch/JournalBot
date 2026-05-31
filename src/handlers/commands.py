import base64
import io
import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.clients.internal_api import get_status, plan_meal, plan_workout, calculate_calories
from src.security import with_security
from src.utils.formatter import format_for_telegram

logger = logging.getLogger(__name__)

@with_security
async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status = await get_status()
    await update.message.reply_text(status)


@with_security
async def handle_plan_meal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Processing /plan_meal")
    description = " ".join(context.args) if context.args else "Standard default plan"
    user_id = str(update.effective_user.id)
    plan_response = await plan_meal(description, user_id)
    result = format_for_telegram(plan_response)
    await update.message.reply_html(result)


@with_security
async def handle_calories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Processing calories calculation from image command")
    message = update.message

    caption_text = message.caption or ""

    # Structural Safety Check: If it's a photo from MessageHandler but doesn't target our command
    if message.photo and not caption_text.startswith("calories"):
        return

    # Fallback Case: User sent text only command without attaching media
    if not message.photo:
        await message.reply_text(
            "Please send a photo of your food, and make sure to include "
            "<b>calories</b> directly inside the photo caption!",
            parse_mode="HTML"
        )
        return

    # Processing Multimodal Image
    user_id = str(update.effective_user.id)
    photo = message.photo[-1]

    file = await context.bot.get_file(photo.file_id)
    image_buffer = io.BytesIO()
    await file.download_to_memory(out=image_buffer)

    # Standardize binary layout to base64
    image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    mime_type = "image/jpeg"

    # Forward payload data arrays outbound to back-end computation engine
    calories_response = await calculate_calories(image_base64, mime_type, user_id)

    result = format_for_telegram(calories_response)
    await message.reply_html(result)


@with_security
async def handle_plan_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Processing /plan_workout")
    description = " ".join(context.args) if context.args else "Standard default plan"
    plan_response = await plan_workout(description)
    result = format_for_telegram(plan_response)
    await update.message.reply_html(result)
