CREATE TABLE account (
    username char(8) NOT NULL,
    password char(8) NOT NULL,
    name varchar(32),
    PRIMARY KEY (username)
);

CREATE TABLE balance (
    balance_id serial,
    username char(8) NOT NULL,
    retrieve_date date NOT NULL,
    amount float(2) NOT NULL,
    PRIMARY KEY (balance_id),

