create table currency (
    id bigint primary key,
    currency varchar(255)
);

create table category (
    codename varchar(255),
    name varchar(255)
);

create table budget (
    id bigint primary key,
    currency integer,
    daily integer,
    weekly integer,
    monthly integer,
    balance integer,

    FOREIGN KEY(currency) REFERENCES currency(id)
);

create table expense (
    id integer primary key,
    amount integer,
    created datetime,
    category varchar(255),
    raw_text text,
    currency integer,
    FOREIGN KEY(category) REFERENCES category(codename),
    FOREIGN KEY(currency) REFERENCES currency(id)
);

insert into currency (id, currency)
values
    (1, "RUB"),
    (2, "EUR"),
    (3, "USD");

insert into category (codename, name)
values
    ("products", "продукты"),
    ("coffee", "кофе"),
    ("cafe", "кафе"),
    ("restaurant", "рестораны"),
    ("subscription", "подписки"),
    ("gifts", "подарки"),
    ("network", "связь и интернет"),
    ("others", "другое"),
    ("transport", "транспорт"),
    ("games", "игры"),
    ("travel", "путешествия");

insert into budget (id, currency, daily, weekly, monthly, balance)
values
    (1, 1, 1500, 10000, 50000, 0),
    (2, 2, 25, 150, 500, 0),
    (3, 3, 30, 170, 700, 0);
