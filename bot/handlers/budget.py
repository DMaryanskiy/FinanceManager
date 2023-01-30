from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from services.budget import retrieve_balance
from services.currency import retrieve_chosen_currency
from singleton import CurrencySingleton

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance_data = await retrieve_balance()
    if not balance_data:
        await send_response(
            update,
            context,
            PROPERTIES["CURRENCY_BAD"]
        )
    else:
        currency = CurrencySingleton()
        currency_code = await retrieve_chosen_currency(currency.instance)
        await send_response(
            update,
            context,
            PROPERTIES["BALANCE"].format(
                balance_data.balance, currency_code.currency,
                balance_data.daily, currency_code.currency,
                balance_data.weekly, currency_code.currency,
                balance_data.monthly, currency_code.currency
            )
    )