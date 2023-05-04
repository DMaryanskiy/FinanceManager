import logging

from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES, QUERIES
from db.db import query_execute
from .response import send_response

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_exists = await query_execute(
        QUERIES["GET_USER"],
        {
            "username": user.username
        }
    )
    if not user_exists:
        row = await query_execute(
            QUERIES["ADD_USER"],
            {
                "username": user.username,
                "firstname": user.first_name,
                "lastname": user.last_name
            }
        )
        user_id = row.first()[0]
        await query_execute(
            QUERIES["CREATE_BALANCE"],
            {
                "id": user_id
            }
        )

    await send_response(update, context, PROPERTIES["GREETINGS"])
