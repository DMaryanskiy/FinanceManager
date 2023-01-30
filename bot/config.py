import os
from pathlib import Path

from dotenv import load_dotenv
from ruamel.yaml import YAML

load_dotenv()

yaml = YAML(typ="safe")
PROPERTIES = yaml.load(open("messages.yml"))
QUERIES = yaml.load(open("queries.yml"))

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"

CURRENCY_MAP = {
    "RUB": "1",
    "EUR": "2",
    "USD": "3",
}

BALANCE_MAP = {
    "expense": QUERIES["REDUCE_BALANCE"],
    "income": QUERIES["ADD_BALANCE"]
}
