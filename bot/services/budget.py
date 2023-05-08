from dataclasses import dataclass
from typing import Optional

from telegram import Update
from sqlalchemy.ext.asyncio import AsyncResult

from db import models
from db.db import get_session
from singleton import CurrencySingleton

@dataclass
class Budget:
    id: int
    currency: int
    balance: int
    telegram_user: int

async def retrieve_balance(update: Update) -> Optional[Budget]:
    session = None
    async for s in get_session():
        session = s

    currency = CurrencySingleton()
    if currency.currency not in {"1", "2", "3"}:
        return None
    
    user_query = models.telegram_user.select().where(
        models.telegram_user.c.username == update.message.from_user.username
    )
    user_row: AsyncResult = await session.execute(user_query)
    user = user_row.one()

    budget_query = models.budget.select().where(
        models.budget.c.currency == int(currency.currency),
        models.budget.c.telegram_user == user._asdict()["id"]
    )
    budget_row: AsyncResult = await session.execute(budget_query)
    budget = budget_row.one()
    return Budget(**budget._asdict())
