from dataclasses import dataclass

from db import fetch_all, fetch_one
from config import QUERIES

@dataclass
class Category:
    id: int
    codename: str

async def get_all_categories() -> list[Category]:
    categories = await fetch_all(QUERIES["GET_CATEGORIES"])
    return [Category(**category) for category in categories]

async def retrieve_category(codename: str) -> Category:
    category = await fetch_one(QUERIES["RETRIVE_CATEGORY"], {"codename": codename})
    if category:
        return Category(**category)
    return category
