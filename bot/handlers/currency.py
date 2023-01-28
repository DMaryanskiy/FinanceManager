import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from services.currency import get_all_currencies
from singleton import CurrencySingleton

async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(
        update,
        context,
        PROPERTIES["CURRENCY"],
        await _currency_keyboard()
    )

async def currency_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not query.data:
        return
    cur = CurrencySingleton()
    cur.data = query.data
    await query.edit_message_text(
        text=PROPERTIES["CURRENCY_BUTTON"].format(query.data),
        parse_mode=telegram.constants.ParseMode.HTML,
    )

async def _currency_keyboard() -> InlineKeyboardMarkup:
    currencies = await get_all_currencies()
    keyboard = [
        [
            InlineKeyboardButton(currency.currency, callback_data=currency.currency) for currency in currencies
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
