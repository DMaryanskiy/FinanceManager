from dataclasses import dataclass
from typing import Optional

from db import fetch_one
from config import QUERIES
from handlers.singleton import CurrencySingleton

@dataclass
class Budget:
    id: int
    currency: int
    daily: int
    weekly: int
    monthly: int
    balance: int

async def retrieve_budget() -> Optional[Budget]:
    currency = CurrencySingleton()
    if not currency:
        return None
    budget = await fetch_one(QUERIES["RETRIEVE_BUDGET"].format(currency.data))
    return Budget(**budget)

