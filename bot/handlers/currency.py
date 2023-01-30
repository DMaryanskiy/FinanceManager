import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from services.currency import get_all_currencies, retrieve_chosen_currency
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
    # storing currency code to transmit through other parts of project.
    cur = CurrencySingleton()
    cur.instance = query.data
    currency_code = await retrieve_chosen_currency(query.data)
    await query.edit_message_text(
        text=PROPERTIES["CURRENCY_BUTTON"].format(currency_code.currency),
        parse_mode=telegram.constants.ParseMode.HTML,
    )

async def _currency_keyboard() -> InlineKeyboardMarkup:
    currencies = await get_all_currencies()
    keyboard = [
        [
            InlineKeyboardButton(currency.currency, callback_data=currency.id) for currency in currencies
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
