import asyncio
import aiosqlite
import logging
from collections.abc import Iterable
from typing import Any

import config

logger = logging.getLogger(__name__)

async def get_db() -> aiosqlite.Connection:
    """ Function for connecting to db. """
    if not getattr(get_db, "db", None):
        db = await aiosqlite.connect(config.SQLITE_DB_FILE)
        get_db.db = db
        logger.info("Connected to db.")
    return get_db.db

async def fetch_all(
    sql: str,
    params: Iterable[Any] | None = None
) -> list[dict]:
    """
    Function for fetching all rows after executing SQL query.
    Args:
        sql: query string.
        params: optional iterative sequence with query params.
    Returns:
        List of row dictionaries {"column": value}.
    """
    cursor = await _get_cursor(sql, params)
    rows = await cursor.fetchall()
    results = []
    for row_ in rows:
        results.append(_get_result_with_column_names(cursor, row_))
    await cursor.close()
    return results

async def fetch_one(
    sql: str,
    params: Iterable[Any] | None = None
) -> dict | None:
    """
    Function for fetching one row after executing SQL query.
    Args:
        sql: query string.
        params: optional iterative sequence with query params.
    Returns:
        Row dictionary {"column": value} or None.
    """
    cursor = await _get_cursor(sql, params)
    row_ = await cursor.fetchone()
    if not row_:
        return None
    row = _get_result_with_column_names(cursor, row_)
    await cursor.close()
    return row

async def execute(
    sql: str,
    params: Iterable[Any] | None = None,
    *,
    autocommit: bool = True
) -> None:
    """
    Function for executing SQL queries like INSERT, UPDATE or DELETE.
    Args:
        sql: query string.
        params: optional iterative sequence with query params.
        autocommit: bool parameter to execute COMMIT statement right after sql query.
    """
    db = await get_db()
    args: tuple[str, Iterable[Any] | None] = (sql, params)
    await db.execute(*args)
    if autocommit:
        await db.commit()

def close_db() -> None:
    """ Function for closing connection to db. """
    asyncio.run(_async_close_db())

async def _async_close_db() -> None:
    logger.info("Closing db.")
    await (await get_db()).close()
    logger.info("Db closed.")

async def _get_cursor(
    sql: str,
    params: Iterable[Any] | None
) -> aiosqlite.Cursor:
    """
    Function for getting cursor of current db connection.
    Args:
        sql: query string.
        params: optional iterative sequence with query params.
    Returns:
        An instance of Cursor class.
    """
    db = await get_db()
    args: tuple[str, Iterable[Any] | None] = (sql, params)
    cursor = await db.execute(*args)
    db.row_factory = aiosqlite.Row
    return cursor

def _get_result_with_column_names(
    cursor: aiosqlite.Cursor,
    row: aiosqlite.Row
) -> dict:
    """
    Function for converting row to dictionary {"column": value}.
    Args:
        cursor: an instance of Cursor class.
        row: an instance of Row class.
    Returns:
        Dictionary {"column": value}.
    """
    column_names = [d[0] for d in cursor.description]
    resulting_row = {}
    for index, column_name in enumerate(column_names):
        resulting_row[column_name] = row[index]
    return resulting_row
