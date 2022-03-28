# E-commerce API

E-commerce API is a simplified part of an e-commerce system that contains data about buyers (customers) and products. It is created using Python's Flask framework.

- Python version: 3.9.5

- Flask version: 2.0.3

- Werkzeug version: 2.0.3

The system allows creating, reading and deleting data.

## 1. Usage

### 1. 1. Creating the database tables

**The database backup file for the project has already been created, and it is provided in the project folder**. However, if for some reason, the database file gets lost, simply run the "create_database.py" file in the project directory and a new (empty) database file will be created.

```bash
python create_database.py
```

### 1. 2. Starting the application
In order to be able to use the application, make sure that the dependencies provided in the "requirements.txt" file are installed on your machine.

You can start the application in one of the following 2 ways:

#### Way 1

1. Set the environment variable FLASK_APP to app.py
2. Run the application by using the "flask run" command

Examples:
- If you are using CMD
```bash
set FLASK_APP=app.py
flask run
```

- If you are using Powershell
```bash
$env:FLASK_APP = "hello"
flask run
```

- If you are using BASH
```bash
export FLASK_APP=app.py
flask run
```

- If you are using Fish
```bash
set -x FLASK_APP hello
flask run
```

#### Way 2

Alternatively, you can start the application by simply running the "app.py" file.

```bash
python app.py
```

### 1. 3. Endpoints
#### /buyers
Displays a list of all buyers (if endpoint is accessed using a "GET" request), and inserts a new buyer into database (if endpoint is accessed using a "POST" request).

If accessed using a "POST" request, his endpoint accepts the inputs provided through form-data that contains the following keys:

- first_name
- last_name
- email
- credit_card
- address_street_name
- address_street_number
- address_zip_code
- address_city
- address_country

**credit_card** is an optional field, so it can be left empty. However, if you do provide a credit card, then it will first be validated. If it is not valid, the function will return false.

In order for **credit_card** to be considered valid, the following criteria must be met:
- It must be of lenght 16
- It must start with 4, 5 or 6
- It can only contain digits (0-9)
- No 4 back-to-back digits can be same 

#### /buyers/delete/<id>
Deletes a buyer with a certain (provided) id. This endpoint can only be accessed by using the "DELETE" method.

#### /products
Displays a list of all products ordered by id (if endpoint is accessed using a "GET" request), and inserts a new product into database (if endpoint is accessed using a "POST" request). There is another endpoint (/products/<desired_currency>) that displays all products sorted by price (from lowest to highest) after converting the price of the products in the desired currency.

If accessed using a "POST" request, his endpoint accepts the inputs provided through form-data that contains the following keys:

- name
- category
- quantity
- size
- price
- currency

All of the abovementioned fields are required.

**category** must be one of the following: Trenerki, pizami, bluzi.

**size** must be one of the following: S, M, L, XL.

**currency** must be one of the following: MKD, EUR, USD.

#### /products/<desired_currency>
Converts the price of all products into desired (provided) currency and displays a list of all products sorted by price in ascending order (from lowest to highest). This endpoint can only be accessed by using the "GET" method.

Each time this endpoint is accessed, in order for the price to be converted into desired currency, a request is made to http://data.fixer.io/api/latest?access_key=13c1d8b6ad2676c9afe6e02c310457fd. The API KEY that is provided is free, but can only be used to make a limited number of requests. That's why the exchange rate conversion process is wrapped in a "try - except" clause. If a request can't be made, the EUR to MKD exchange rate is hard coded to 61.63, and the EUR to USD exchange rate is hard coded to 1.10.

#### /products/delete/<id>
Deletes a buyer with a certain (provided) id. This endpoint can only be accessed by using the "DELETE" method.
