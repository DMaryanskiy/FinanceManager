import datetime
import logging

import pytz

from db import execute
from config import QUERIES, CURRENCY_MAP, PROPERTIES, BALANCE_MAP

logger = logging.getLogger(__name__)

async def expenses_(category: str, typ: str, amount: str, currency: str) -> str:
    created = _get_now_datetime()
    if typ == "expense" or typ == "income":
        await execute("BEGIN")
        await execute(
            QUERIES["ADD_EXPENSE"].format(typ), {
            "amount": amount,
            "created": created,
            "category": category,
            "currency": CURRENCY_MAP[currency]
            },
            autocommit=False
        )
        logger.info("Added expense.")
        await execute(
            BALANCE_MAP[typ], {
            "amount": amount,
            "currency": CURRENCY_MAP[currency]
            },
            autocommit=False
        )
        logger.info("Updated balance.")
        await execute("COMMIT")
        return PROPERTIES["EXPENSES_GOOD"].format(typ)
    else:
        return PROPERTIES["WRONG_TYPE"]

def _get_now_datetime() -> str:
    timezone = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(timezone)
    return now.strftime("%Y-%m-%d %H:%M:%S")
