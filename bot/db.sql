create table currency (
    id bigint primary key,
    currency varchar(255)
);

create table category (
    id bigint primary key,
    codename varchar(255)
);

create table transaction_type (
    id bigint primary key,
    codename varchar(255)
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
    currency integer,
    transaction_type varchar(255),

    FOREIGN KEY(category) REFERENCES category(id),
    FOREIGN KEY(currency) REFERENCES currency(id),
    FOREIGN KEY(transaction_type) REFERENCES transaction_type(id)
);

insert into currency (id, currency)
values
    (1, "RUB"),
    (2, "EUR"),
    (3, "USD");

insert into transaction_type (id, codename)
values
    (1, "expense"),
    (2, "income");

insert into category (id, codename)
values
    (1, "products"),
    (2, "coffee"),
    (3, "cafe"),
    (4, "restaurant"),
    (5, "subscription"),
    (6, "gifts"),
    (7, "network"),
    (8, "transport"),
    (9, "games"),
    (10, "travel"),
    (11, "other expenses"),
    (12, "salary"),
    (13, "festival"),
    (14, "social"),
    (15, "family"),
    (16, "other income");

insert into budget (id, currency, daily, weekly, monthly, balance)
values
    (1, 1, 1500, 10000, 50000, 0),
    (2, 2, 25, 150, 500, 0),
    (3, 3, 30, 170, 700, 0);
