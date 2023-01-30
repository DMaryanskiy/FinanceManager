from dataclasses import dataclass
from typing import Optional

from db import fetch_one
from config import QUERIES
from singleton import CurrencySingleton

@dataclass
class Budget:
    id: int
    currency: int
    daily: int
    weekly: int
    monthly: int
    balance: int

async def retrieve_balance() -> Optional[Budget]:
    currency = CurrencySingleton()
    if currency.instance not in {"1", "2", "3"}:
        return None
    budget = await fetch_one(QUERIES["RETRIEVE_BUDGET"], {"currency": currency.instance})
    return Budget(**budget)
