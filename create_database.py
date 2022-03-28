import sqlite3

db = sqlite3.connect('database.sqlite3')

db = db.cursor()

db.execute(""" CREATE TABLE IF NOT EXISTS buyers (
    id integer PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text NOT NULL,
    credit_card text,
    profile_created datetime NOT NULL,
    address_street_name text NOT NULL,
    address_street_number text NOT NULL,
    address_zip_code text NOT NULL,
    address_city text NOT NULL,
    address_country text NOT NULL
) """)

db.execute(""" CREATE TABLE IF NOT EXISTS products (
    id integer PRIMARY KEY,
    product_name text NOT NULL,
    product_category text NOT NULL,
    quantity int NOT NULL,
    size text NOT NULL,
    price numeric NOT NULL,
    currency text NOT NULL
) """)