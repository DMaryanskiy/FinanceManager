from dataclasses import asdict

from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from singleton import CurrencySingleton

def get_value_currency(object: object, currency: str) -> list[str]:
    """
    Function to get a list with sequent pairs "amount, currency, amount, currency...".
    Args:
        object: class instance (Budget and Expense in this case).
        currency: curreny code as string.
    """
    result = []
    for _, value in asdict(object).items():
        result += [value, currency]
    
    return result

async def validate_currency(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    currency: CurrencySingleton
) -> bool:
    if currency.currency not in {"1", "2", "3"}:
        await send_response(
            update,
            context,
            PROPERTIES["CURRENCY_BAD"]
        )
        return False
    return True

async def validate_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    currency: CurrencySingleton
) -> bool:
    if not await validate_currency(update, context, currency):
        return False
    
    user_message = update.message.text
    if len(user_message.split()) != 3:
        await send_response(
            update,
            context,
            PROPERTIES["MESSAGE_BAD"]
        )
        return False
    
    return True
