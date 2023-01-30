from dataclasses import dataclass
from typing import Optional

from db import fetch_one
from config import QUERIES, CURRENCY_MAP
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
    if not hasattr(currency, "data"):
        return None
    budget = await fetch_one(QUERIES["RETRIEVE_BUDGET"], {"currency": CURRENCY_MAP[currency.data]})
    return Budget(**budget)
