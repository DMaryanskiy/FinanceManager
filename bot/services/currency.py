import logging
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from db import models
from db.db import get_session
from singleton import SessionSingleton

logger = logging.getLogger(__name__)


@dataclass
class Currency:
    id: int
    currency_code: str

async def get_all_currencies() -> list[Currency]:
    session = SessionSingleton().session
    currencies_query = models.currency.select()
    currencies_rows: AsyncResult = await session.execute(currencies_query)
    currencies = currencies_rows.all()
    return [Currency(**currency._asdict()) for currency in currencies]

async def retrieve_chosen_currency(id: str) -> Currency:
    session = SessionSingleton().session
    currencies_query = models.currency.select().where(models.currency.c.id == int(id))
    currencies_rows: AsyncResult = await session.execute(currencies_query)
    currency = currencies_rows.one()
    return Currency(**currency._asdict())
