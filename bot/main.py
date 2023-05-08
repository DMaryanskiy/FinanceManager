import argparse
import asyncio
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
import singleton
from db.db import init_db, insert_prereq, get_session

logging.basicConfig(
    filename="main.log",
    format="%(asctime)s,%(msecs)d:%(levelname)s:%(name)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

if not config.BOT_TOKEN:
    exit("Specify BOT_TOKEN env variable.")

async def startup() -> None:
    await init_db()
    logger.info("bot started")

    ss = singleton.SessionSingleton()
    async for s in get_session():
        ss.session = s

def bot_start():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    COMMAND_HANDLERS = {
        "start": handlers.start,
        "currency": handlers.currency,
        "balance": handlers.balance,
        "category": handlers.category,
        "help": handlers.help,
    #     "statistics": handlers.statistics
    }

    for command_name, handler in COMMAND_HANDLERS.items():
        app.add_handler(CommandHandler(command_name, handler))

    app.add_handler(CallbackQueryHandler(handlers.currency_button))

    # app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.expenses_limits))

    app.run_polling()

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        startup_task = loop.create_task(startup())
        loop.run_until_complete(startup_task)

        parser = argparse.ArgumentParser(description="Command to run a bot")
        parser.add_argument("-i", "--insert", action='store_true', help="Insert prerequisites to db.")

        args = parser.parse_args()
        if args.insert:
            insert_task = loop.create_task(insert_prereq())
            loop.run_until_complete(insert_task)

        bot_start()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())

if __name__ == "__main__":
    main()
