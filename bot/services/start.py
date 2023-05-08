import logging

from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.exc import IntegrityError
from telegram import Update

from db.db import get_session, session_commit
from db import models
from singleton import SessionSingleton
from .exceptions import HTTPException

logger = logging.getLogger(__name__)

async def get_or_create_user(update: Update):
    """
    Function checks whether user already exists in DB.
    If not, it creates user and budget instances in DB.
    """
    # TODO: find a way to fix session receiving operation 
    ss = SessionSingleton()
    session = ss.session

    user = update.message.from_user
    user_exists_query = models.telegram_user.select().where(models.telegram_user.c.username == user.username)
    user_result: AsyncResult = await session.execute(user_exists_query)
    user_exists = user_result.one_or_none() # get user
    if not user_exists:
        user_data = {
            "username": user.username,
            "firstname": user.first_name,
            "lastname": user.last_name
        }

        user_create_query = models.telegram_user.insert().values(**user_data)
        user_result: AsyncResult = await session.execute(user_create_query) # create user

        logger.info("user created")

        last_user_id: int = user_result.inserted_primary_key[0]

        for i in range(1, 4):
            budget_data = {
                "currency": i,
                "balance": 0,
                "telegram_user": last_user_id
            }
            budget_create_query = models.budget.insert().values(**budget_data) # create budget
            await session.execute(budget_create_query)
        
        logger.info("budget created")

        await session_commit(IntegrityError, HTTPException("user already exists in DB."), session)
