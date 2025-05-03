import sqlite3
from hashlib import sha256
import re

def validate_user_data(cc_number, cc_valid, cvc):
    # Remove all spaces in the credit card number
    clean_cc = re.sub(r"\s+", "", cc_number)
    if not re.fullmatch(r'\d{16}', clean_cc):
        raise ValueError(f"Invalid credit card number: {cc_number}")
    if not re.fullmatch(r'(0[1-9]|1[0-2])/([0-9]{2})', cc_valid):
        raise ValueError(f"Invalid expiry date format: {cc_valid}")
    if not re.fullmatch(r'\d{3}', cvc):
        raise ValueError(f"Invalid CVC format: {cvc}")

with open("schema.sql") as f:
    sql = f.read()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     first_name TEXT NOT NULL,
     last_name TEXT NOT NULL,
     user_id TEXT NOT NULL UNIQUE,
     cc_number TEXT NOT NULL,
     cc_valid TEXT NOT NULL,
     cvc TEXT NOT NULL,
     username TEXT NOT NULL UNIQUE,
     password TEXT NOT NULL,
     is_admin INTEGER NOT NULL DEFAULT 0 )
''')
users = [
    {
        "first_name": "Admin",
        "last_name": "User",
        "user_id": "111111111",
        "cc_number": "1234 5678 9012 3456",
        "cc_valid": "12/30",
        "cvc": "123",
        "username": "admin",
        "password": "admin123",
        "is_admin": 1
    },
    {
        "first_name": "Israeli",
        "last_name": "Israelii",
        "user_id": "123456789",
        "cc_number": "1234 5567 8901 2345",
        "cc_valid": "12/32",
        "cvc": "123",
        "username": "israeli",
        "password": "israeli123",
        "is_admin": 0
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "user_id": "222222222",
        "cc_number": "4321 1234 5678 8765",
        "cc_valid": "11/29",
        "cvc": "234",
        "username": "john",
        "password": "john123",
        "is_admin": 0
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "user_id": "333333333",
        "cc_number": "5555 4444 3333 2222",
        "cc_valid": "10/28",
        "cvc": "345",
        "username": "jane",
        "password": "jane123",
        "is_admin": 0
    },
    {
        "first_name": "Ali",
        "last_name": "Khan",
        "user_id": "444444444",
        "cc_number": "1111 2222 3333 4444",
        "cc_valid": "01/30",
        "cvc": "456",
        "username": "ali",
        "password": "ali123",
        "is_admin": 0
    },
    {
        "first_name": "Sara",
        "last_name": "Lee",
        "user_id": "555555555",
        "cc_number": "9999 8888 7777 6666",
        "cc_valid": "06/27",
        "cvc": "567",
        "username": "sara",
        "password": "sara123",
        "is_admin": 0
    },
    {
        "first_name": "Noor",
        "last_name": "Ahmed",
        "user_id": "666666666",
        "cc_number": "1212 3434 5656 7878",
        "cc_valid": "04/26",
        "cvc": "678",
        "username": "noor",
        "password": "noor123",
        "is_admin": 0
    },
    {
        "first_name": "Mike",
        "last_name": "Jordan",
        "user_id": "777777777",
        "cc_number": "2468 1357 2468 1357",
        "cc_valid": "07/29",
        "cvc": "789",
        "username": "mike",
        "password": "mike123",
        "is_admin": 0
    },
    {
        "first_name": "Huda",
        "last_name": "Ali",
        "user_id": "888888888",
        "cc_number": "1020 3040 5060 7080",
        "cc_valid": "09/25",
        "cvc": "890",
        "username": "huda",
        "password": "huda123",
        "is_admin": 0
    },
    {
        "first_name": "Yousef",
        "last_name": "Omar",
        "user_id": "999999999",
        "cc_number": "1111 9999 8888 7777",
        "cc_valid": "08/31",
        "cvc": "901",
        "username": "yousef",
        "password": "yousef123",
        "is_admin": 0
    }
]
for user in users:
    try:
        validate_user_data(user["cc_number"], user["cc_valid"], user["cvc"])
        hashed_password = sha256(user["password"].encode()).hexdigest()
        cursor.execute('''
    INSERT INTO users (first_name, last_name, user_id, cc_number, cc_valid, cvc, username, password, is_admin)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    user["first_name"], user["last_name"], user["user_id"],
    user["cc_number"], user["cc_valid"], user["cvc"],
    user["username"], hashed_password, user["is_admin"]
))
        print(f"Inserted user: {user['username']}")
    except Exception as e:
        print(f"Failed to insert user {user['username']}: {e}")

conn.commit()
conn.close()
print("Database initialized with 10 users.")