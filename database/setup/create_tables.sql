CREATE TABLE account (
    username char(8) NOT NULL,
    password char(8) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE balance (
    id serial,
    username char(8) NOT NULL,
    retrieve_date date NOT NULL,
    amount float(2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account
);

CREATE TABLE subscription (
    id serial,
    username char(8) NOT NULL,
    amount float(2) NOT NULL,
    chat_id integer NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account,
    CONSTRAINT unique_sub UNIQUE (username, amount, chat_id)
);
