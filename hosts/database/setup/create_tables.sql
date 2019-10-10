CREATE TABLE account (
    username CHAR(8) NOT NULL,
    password CHAR(8) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT TIMEZONE('Asia/Singapore', now()),
    PRIMARY KEY (username)
);

CREATE TABLE balance (
    id SERIAL,
    username CHAR(8) NOT NULL,
    retrieve_date DATE NOT NULL,
    amount FLOAT(2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT TIMEZONE('Asia/Singapore', now()),
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account
);

CREATE TABLE subscription (
    id SERIAL,
    username CHAR(8) NOT NULL,
    amount FLOAT(2) NOT NULL,
    chat_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT TIMEZONE('Asia/Singapore', now()),
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account,
    CONSTRAINT unique_sub UNIQUE (username, amount, chat_id)
);

CREATE TABLE notification (
    id SERIAL,
    username CHAR(8) NOT NULL,
    chat_id INTEGER NOT NULL,
    message_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT TIMEZONE('Asia/Singapore', now()),
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES account
);

CREATE TABLE command (
    id SERIAL,
    name VARCHAR(32) NOT NULL,
    chat_id INTEGER NOT NULL,
    is_cancelled BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT TIMEZONE('Asia/Singapore', now()),
    PRIMARY KEY (id)
);

CREATE VIEW ordered_balances AS (
    SELECT * FROM balance ORDER BY id DESC
);

CREATE VIEW num_users AS (
    SELECT num_acc, num_sub
    FROM (SELECT COUNT(*) AS num_acc FROM account) AS a,
        (SELECT COUNT(*) AS num_sub FROM subscription) AS s
);

CREATE VIEW stats AS (
    SELECT 'account' AS table_name, COUNT(1) AS counts
    FROM account

    UNION ALL

    SELECT 'balance' AS table_name, COUNT(1) AS counts
    FROM balance

    UNION ALL

    SELECT 'subscription' AS table_name, COUNT(1) AS counts
    FROM subscription

    UNION ALL

    SELECT 'notification' AS table_name, COUNT(1) AS counts
    FROM notification
);
