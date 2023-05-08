from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncResult

from db import models
from config import QUERIES
from singleton import SessionSingleton

@dataclass
class Category:
    id: int
    codename: str

async def get_all_categories() -> list[Category]:
    session = SessionSingleton().session
    categories_query = models.category.select()
    categories_rows: AsyncResult = await session.execute(categories_query)
    categories = categories_rows.all()
    return [Category(**category._asdict()) for category in categories]

async def retrieve_category(codename: str) -> Category:
    session = SessionSingleton().session
    categories_query = models.category.select().where(models.category.c.codename == codename)
    categories_rows: AsyncResult = await session.execute(categories_query)
    category = categories_rows.one()
    return Category(**category._asdict())
