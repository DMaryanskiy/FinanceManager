import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters
)

import config
import handlers
from db import close_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not config.BOT_TOKEN:
    exit("Specify BOT_TOKEN env variable.")

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    COMMAND_HANDLERS = {
        "start": handlers.start,
        "currency": handlers.currency,
        "balance": handlers.balance,
        "category": handlers.category,
        "help": handlers.help,
        "statistics": handlers.statistics
    }

    for command_name, handler in COMMAND_HANDLERS.items():
        app.add_handler(CommandHandler(command_name, handler))

    app.add_handler(CallbackQueryHandler(handlers.currency_button))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.expenses_limits))

    app.run_polling()

try:
    main()
except Exception:
    import traceback

    logger.warning(traceback.format_exc())
finally:
    close_db()
