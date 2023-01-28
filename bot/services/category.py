from dataclasses import dataclass

from db import fetch_all
from config import QUERIES

@dataclass
class Category:
    codename: str
    name: str

async def get_all_categories() -> list[Category]:
    categories = await fetch_all(QUERIES["GET_CATEGORIES"])
    return [Category(**category) for category in categories]
