from telegram import Update
from telegram.ext import ContextTypes

from config import PROPERTIES
from .response import send_response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update, context, PROPERTIES["GREETINGS"])
