from sqlalchemy import Column, DateTime, ForeignKey, func, Integer,\
    PrimaryKeyConstraint, String, Table
from sqlalchemy.orm import DeclarativeBase

from .db import metadata


class Base(DeclarativeBase):
    pass


currency = Table(
    "currency",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("currency_code", String)
)

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("codename", String)
)

transaction_type = Table(
    "transaction_type",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("codename", String)
)

telegram_user = Table(
    "telegram_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("firstname", String),
    Column("lastname", String)
)

budget = Table(
    "budget",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("currency", Integer, ForeignKey("currency.id")),
    Column("balance", Integer),
    Column("telegram_user", Integer, ForeignKey("telegram_user.id"))
)

expense = Table(
    "expense",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("amount", Integer),
    Column("created", DateTime, server_default=func.now()),
    Column("category", Integer, ForeignKey("category.id")),
    Column("currency", Integer, ForeignKey("currency.id")),
    Column("transaction_type", Integer, ForeignKey("transaction_type.id")),
    Column("telegram_user", Integer, ForeignKey("telegram_user.id"))
)


class Currency(Base):
    __table__ = currency


class Category(Base):
    __table__ = category


class TransactionType(Base):
    __table__ = transaction_type


class TelegramUser(Base):
    __table__ = telegram_user


class Budget(Base):
    __table__ = budget


class Expense(Base):
    __table__ = expense
