CREATE TABLE account (
    username CHAR(8) NOT NULL,
    password CHAR(8) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE balance (
    id SERIAL,
    username CHAR(8) NOT NULL,
    retrieve_date DATE NOT NULL,
    amount FLOAT(2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account
);

CREATE TABLE subscription (
    id SERIAL,
    username CHAR(8) NOT NULL,
    amount FLOAT(2) NOT NULL,
    chat_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account,
    CONSTRAINT unique_sub UNIQUE (username, amount, chat_id)
);

CREATE TABLE notification(
    id SERIAL,
    username CHAR(8) NOT NULL,
    chat_id INTEGER NOT NULL,
    message_date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account
);

CREATE VIEW ordered_balances AS (
    SELECT * FROM balance ORDER BY id DESC
);

CREATE VIEW num_users AS (
    SELECT num_acc, num_sub
    FROM (SELECT COUNT(*) AS num_acc FROM account) AS a,
        (SELECT COUNT(*) AS num_sub FROM subscription) AS s
);
