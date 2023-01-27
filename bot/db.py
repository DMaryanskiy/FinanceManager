import asyncio
import aiosqlite
import logging
from collections.abc import Iterable
from typing import Any, Optional

import config

logger = logging.getLogger(__name__)

async def get_db() -> aiosqlite.Connection:
    if not getattr(get_db, "db", None):
        db = await aiosqlite.connect(config.SQLITE_DB_FILE)
        get_db.db = db
        logger.info("Connected to db.")
    return get_db.db

async def fetch_all(
    sql: str,
    params: Optional[Iterable[Any]] = None
) -> list[dict]:
    cursor = await _get_cursor(sql, params)
    rows = await cursor.fetchall()
    results = []
    for row_ in rows:
        results.append(_get_result_with_column_names(cursor, row_))
    await cursor.close()
    return results

async def fetch_one(
    sql: str,
    params: Optional[Iterable[Any]] = None
) -> dict | None:
    cursor = await _get_cursor(sql, params)
    row_ = await cursor.fetchone()
    if not row_:
        return None
    row = _get_result_with_column_names(cursor, row_)
    await cursor.close()
    return row

def close_db() -> None:
    asyncio.run(_async_close_db())

async def _async_close_db() -> None:
    logger.info("Closing db.")
    await (await get_db()).close()
    logger.info("Db closed.")

async def _get_cursor(
    sql: str,
    params: Optional[Iterable[Any]]
) -> aiosqlite.Cursor:
    db = await get_db()
    args: tuple[str, Optional[Iterable[Any]]] = (sql, params)
    cursor = await db.execute(*args)
    db.row_factory = aiosqlite.Row
    return cursor

def _get_result_with_column_names(
    cursor: aiosqlite.Cursor,
    row: aiosqlite.Row
) -> dict:
    column_names = [d[0] for d in cursor.description]
    resulting_row = {}
    for index, column_name in enumerate(column_names):
        resulting_row[column_name] = row[index]
    return resulting_row
