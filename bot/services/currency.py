from dataclasses import dataclass

from db import fetch_all, fetch_one
from config import QUERIES

@dataclass
class Currency:
    id: int
    currency: str

async def get_all_currencies() -> list[Currency]:
    currencies = await fetch_all(QUERIES["GET_CURRENCIES"])
    return [Currency(**currency) for currency in currencies]

async def retrieve_chosen_currency(id: str) -> Currency:
    currency = await fetch_one(QUERIES["RETRIEVE_CHOSEN_CURRENCY"], {"id": id})
    return Currency(**currency)
