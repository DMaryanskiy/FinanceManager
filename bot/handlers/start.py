from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response
from services.start import get_or_create_user

async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE,
            ):
    
    await get_or_create_user(update)
    
    await send_response(update, context, PROPERTIES["GREETINGS"])
