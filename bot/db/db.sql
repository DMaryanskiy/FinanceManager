create table if not exists currency (
    id bigint primary key,
    currency_code varchar(255)
);
create table if not exists category (
    id bigint primary key,
    codename varchar(255)
);
create table if not exists transaction_type (
    id bigint primary key,
    codename varchar(255)
);
create table if not exists telegram_user (
    id bigint primary key,
    username varchar(255),
    firstname varchar(255),
    lastname varchar(255)
);
create table if not exists budget (
    id bigint primary key,
    currency integer,
    balance integer,
    telegram_user integer,

    FOREIGN KEY(currency) REFERENCES currency(id),
    FOREIGN KEY(telegram_user) REFERENCES telegram_user(id)
);
create table if not exists expense (
    id integer primary key,
    amount integer,
    created timestamp,
    category integer,
    currency integer,
    transaction_type integer,
    telegram_user integer,

    FOREIGN KEY(category) REFERENCES category(id),
    FOREIGN KEY(currency) REFERENCES currency(id),
    FOREIGN KEY(transaction_type) REFERENCES transaction_type(id),
    FOREIGN KEY(telegram_user) REFERENCES telegram_user(id)
);