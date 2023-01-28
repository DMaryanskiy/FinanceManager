import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
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

    app.add_handler(CommandHandler("start", handlers.start))

    app.add_handler(CommandHandler("currency", handlers.currency))
    app.add_handler(CallbackQueryHandler(handlers.currency_button))

    app.add_handler(CommandHandler("balance", handlers.balance))

    app.add_handler(CommandHandler("category", handlers.category))

    app.run_polling()

try:
    main()
except Exception:
    import traceback

    logger.warning(traceback.format_exc())
finally:
    close_db()
