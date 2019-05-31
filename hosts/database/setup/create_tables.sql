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
