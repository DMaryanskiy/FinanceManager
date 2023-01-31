import datetime
import logging
from dataclasses import dataclass

import pytz

from db import execute, fetch_one
from config import QUERIES, PROPERTIES, BALANCE_MAP

logger = logging.getLogger(__name__)

@dataclass
class Statistics:
    daily_expense: int | None
    daily_income: int | None
    weekly_expense: int | None
    weekly_income: int | None
    monthly_expense: int | None
    monthly_income: int | None

async def expenses_(category: str, typ: str, amount: str, currency: str) -> str:
    created = _get_now_datetime_str()
    if typ == "expense" or typ == "income":
        await execute("BEGIN")
        await execute(
            QUERIES["ADD_EXPENSE"].format(typ), {
            "amount": amount,
            "created": created,
            "category": category,
            "currency": currency
            },
            autocommit=False
        )
        logger.info("Added expense.")
        await execute(
            BALANCE_MAP[typ], {
            "amount": amount,
            "currency": currency
            },
            autocommit=False
        )
        logger.info("Updated balance.")
        await execute("COMMIT")
        return PROPERTIES["EXPENSES_GOOD"].format(typ)
    else:
        return PROPERTIES["WRONG_TYPE"]

async def statistics_() -> Statistics:
    statistics_dict = {}
    start_week = _get_start_of_week_str()
    now = _get_now_datetime()
    start_month = f"{now.year:04d}-{now.month:02d}-01"
    STAT_PARAMS = {
        "daily": None,
        "weekly": {"created": start_week},
        "monthly": {"created": start_month}
    }
    for field in Statistics.__dataclass_fields__:
        stats_type, transaction_type = field.split("_")
        temp = await fetch_one(
            QUERIES[f"{stats_type.upper()}_EXPENSE"].format(field, transaction_type),
            STAT_PARAMS[stats_type]
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