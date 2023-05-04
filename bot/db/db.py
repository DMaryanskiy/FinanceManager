import io
import logging
from typing import AsyncIterable

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import config

logger = logging.getLogger(__name__)

engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL, future=True)
metadata = sqlalchemy.MetaData()

async def query_execute_from_file(conn: AsyncConnection, f: io.TextIOWrapper):
    text = f.read().split(";")
    for statement in text:
        if statement:
            command = statement + ";"
            query = sqlalchemy.text(command)
            await conn.execute(query)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def insert_prereq():
    async with engine.begin() as conn:
        with open(config.BASE_DIR / 'db/insert.sql') as f:
            try:
                await query_execute_from_file(conn, f)
            except Exception:
                pass

async def get_session() -> AsyncIterable[AsyncSession]:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def session_commit(error, exception: Exception, session: AsyncSession):
    try:
        await session.commit()
    except error as _:
        await session.rollback()
        raise exception

async def query_execute(statement: str, params: dict[str, str]) -> sqlalchemy.Result | None:
    async for session in get_session():
        return await session.execute(sqlalchemy.text(statement), params)
