import datetime
import logging
from dataclasses import dataclass

import pytz

from db import execute, fetch_one
from config import QUERIES, PROPERTIES
from singleton import CurrencySingleton
from .category import retrieve_category

logger = logging.getLogger(__name__)

@dataclass
class Statistics:
    daily_expense: int | None
    daily_income: int | None
    weekly_expense: int | None
    weekly_income: int | None
    monthly_expense: int | None
    monthly_income: int | None

TRANSACTION_MAP = {
    "expense": (1, QUERIES["REDUCE_BALANCE"]),
    "income": (2, QUERIES["ADD_BALANCE"]),
}

async def expenses_limits_(category: str, typ: str, amount: int, currency: str) -> str | None:
    created = _get_now_datetime_str()
    category_id = await retrieve_category(category)
    if not category_id:
        return PROPERTIES["CATEGORY_BAD"]
    if typ in {"expense", "income"}:
        await execute("BEGIN")
        await execute(
            QUERIES["ADD_EXPENSE"], {
            "amount": amount,
            "created": created,
            "category": category_id.id,
            "currency": currency,
            "transaction_type": TRANSACTION_MAP[typ][0]
            },
            autocommit=False
        )
        logger.info("Added expense.")
        await execute(
            TRANSACTION_MAP[typ][1], {
            "amount": amount,
            "currency": currency
            },
            autocommit=False
        )
        logger.info("Updated balance.")
        await execute("COMMIT")
        return PROPERTIES["EXPENSES_GOOD"].format(typ)
    # elif typ == "update":
    #     if category not in {"daily", "weekly", "monthly"}:
    #         return PROPERTIES["LIMIT_BAD"]
    #     await execute("BEGIN")
    #     await execute(
    #         QUERIES["UPDATE_LIMIT"].format(category),
    #         {
    #             "value": amount,
    #             "currency": currency
    #         },
    #         autocommit=False
    #     )
    #     logger.info(f"{category.capitalize()} limit updated.")
    #     await execute("COMMIT")
    #     return PROPERTIES["LIMITS_UPDATED"].format(category)
    else:
        return PROPERTIES["WRONG_TYPE"]

async def statistics_() -> Statistics:
    currency = CurrencySingleton()
    statistics_dict = {}
    start_week = _get_start_of_week_str()
    now = _get_now_datetime()
    start_month = f"{now.year:04d}-{now.month:02d}-01"
    COMMON_PARAMS = {
        "currency": currency.currency,
    }
    STAT_PARAMS = {
        "daily": COMMON_PARAMS,
        "weekly": {"created": start_week} | COMMON_PARAMS,
        "monthly": {"created": start_month} | COMMON_PARAMS
    }
    for field in Statistics.__dataclass_fields__:
        stats_type, transaction_type = field.split("_")
        temp = await fetch_one(
            QUERIES[f"{stats_type.upper()}_EXPENSE"].format(field),
            STAT_PARAMS[stats_type] | {
                "transaction_type": TRANSACTION_MAP[transaction_type][0]
            }
        )
        if not temp[field]:
            temp[field] = 0
        statistics_dict |= temp
    
    statistics = Statistics(**statistics_dict)
    return statistics

def _get_now_datetime() -> datetime.datetime:
    timezone = pytz.timezone("Europe/Moscow")
    return datetime.datetime.now(timezone)

def _get_now_datetime_str() -> str:
    now =_get_now_datetime()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def _get_start_of_week_str() -> str:
    now = _get_now_datetime()
    dt = now - datetime.timedelta(days=now.weekday())
    return dt.strftime("%Y-%m-%d")
