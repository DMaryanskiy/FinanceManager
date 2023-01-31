from dataclasses import dataclass

from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from .utils import get_value_currency
from services.budget import retrieve_balance
from services.currency import retrieve_chosen_currency
from singleton import CurrencySingleton

@dataclass
class BalanceData:
    balance: int
    daily: int
    weekly: int
    monthly: int

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    budget = await retrieve_balance()
    if not budget:
        await send_response(
            update,
            context,
            PROPERTIES["CURRENCY_BAD"]
        )
        return
    balance_data = BalanceData(
        budget.balance,
        budget.daily,
        budget.weekly,
        budget.monthly
    )
    currency = CurrencySingleton()
    currency_code = await retrieve_chosen_currency(currency.currency)
    await send_response(
        update,
        context,
        PROPERTIES["BALANCE"].format(
            *get_value_currency(balance_data, currency_code.currency)
        )
    )
