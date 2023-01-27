from dataclasses import dataclass

from db import fetch_all
from config import QUERIES

@dataclass
class Currency:
    id: int
    currency: str

async def get_all_currencies() -> list[Currency]:
    currencies = await fetch_all(QUERIES["GET_CURRENCIES"])
    return [Currency(**currency) for currency in currencies]
