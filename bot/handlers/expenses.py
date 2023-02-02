from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from .utils import get_value_currency, validate_currency, validate_message
from services.expenses import expenses_limits_, statistics_
from services.currency import retrieve_chosen_currency
from singleton import CurrencySingleton

async def expenses_limits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = CurrencySingleton()
    if not await validate_message(update, context, currency):
        return
    
    user_message = update.message.text
    typ, amount, category = user_message.split()
    response = await expenses_limits_(category, typ.lower(), amount, currency.currency)
    if response:
        await send_response(update, context, response)
    return

async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = CurrencySingleton()
    if not await validate_currency(update, context, currency):
        return
    currency_code = await retrieve_chosen_currency(currency.currency)
    statistics = await statistics_()
    await send_response(
        update,
        context,
        PROPERTIES["STATISTICS"].format(
            *get_value_currency(statistics, currency_code.currency)
        )
    )
