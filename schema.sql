DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    national_id TEXT NOT NULL,
    credit_card_number TEXT NOT NULL,
    valid_date TEXT NOT NULL,
    cvc TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
);
