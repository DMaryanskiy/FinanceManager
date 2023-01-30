from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from services.expenses import expenses_
from singleton import CurrencySingleton

async def expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = CurrencySingleton()
    if not hasattr(currency, "data"):
        await send_response(
            update,
            context,
            PROPERTIES["CURRENCY_BAD"]
        )
        return

    user_message = update.message.text
    if len(user_message.split()) != 3:
        await send_response(
            update,
            context,
            PROPERTIES["EXPENSES_BAD"]
        )
        return
    typ, amount, category = user_message.split()
    response = await expenses_(category, typ.lower(), amount, currency.data)
    await send_response(update, context, response)
