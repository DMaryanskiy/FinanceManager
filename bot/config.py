import os
from pathlib import Path

from dotenv import load_dotenv
from ruamel.yaml import YAML

load_dotenv()

# YAML configuration.
yaml = YAML(typ="safe")
PROPERTIES = yaml.load(open("messages.yml")) # Messages texts.
QUERIES = yaml.load(open("queries.yml")) # SQL queries.

# Telegram bot token configuration.
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Base path configuration.
BASE_DIR = Path(__file__).resolve().parent

# Database init.
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "")
