from dataclasses import dataclass

from db import fetch_all
from config import QUERIES

@dataclass
class Category:
    codename: str
    name: str

async def get_all_categories() -> list[Category]:
    # FULL OUTER JOIN doesn't work in aiosqlite and UNION returns rows without order.
    categories_outcome = await fetch_all(QUERIES["GET_CATEGORIES_EXPENSE"])
    categories_income = await fetch_all(QUERIES["GET_CATEGORIES_INCOME"])
    categories = categories_outcome + categories_income
    return [Category(**category) for category in categories]
