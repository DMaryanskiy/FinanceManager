from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from .utils import get_value_currency
from services.expenses import expenses_, statistics_
from services.currency import retrieve_chosen_currency
from singleton import CurrencySingleton

async def expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = CurrencySingleton()
    if currency.instance not in {"1", "2", "3"}:
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
    response = await expenses_(category, typ.lower(), amount, currency.instance)
    await send_response(update, context, response)

async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = CurrencySingleton()
    if currency.instance not in {"1", "2", "3"}:
        await send_response(
            update,
            context,
            PROPERTIES["CURRENCY_BAD"]
        )
        return
    
    currency_code = await retrieve_chosen_currency(currency.instance)
    statistics = await statistics_()
    await send_response(
        update,
        context,
        PROPERTIES["STATISTICS"].format(
            *get_value_currency(statistics, currency_code.currency)
        )
    )
