from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from services.category import get_all_categories

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = await get_all_categories()
    categories_edited = [category.codename for category in categories]
    await send_response(
        update,
        context,
        PROPERTIES["CATEGORIES"].format(*categories_edited)
    )
