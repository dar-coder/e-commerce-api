import requests, json

def is_valid(credit_card):
    """ Validate a credit card number 
    In order for the number to be valid, the following criteria must be met:
    - It must be of lenght 16
    - It must start with 4, 5 or 6
    - It can only contain digits (0-9)
    - No 4 back-to-back digits can be same
    The function retirns True if all the criteria are met (collectively). Otherwise, it returns False, along with an explanation """

    # Check if credit card number contains exactly 16 digits
    if len(credit_card) != 16:
        return False, "Credit card number must be of length 16"

    # Check if credit card number starts with 4, 5 or 6
    if credit_card.startswith("4") or credit_card.startswith("5") or credit_card.startswith("6"):
        pass
    else:
        return False, "Credit card number must start with 4, 5 or 6"

    # Check if credit number contains only digits. If it can be converted from string to integer, then it is True, else it is False
    try:
        credit_card_integer = int(credit_card)
    except:
        return False, "Credit card number must contain only digits"
    
    # Check if any 4 back-to-back digits are same
    # Starting from the first digit and going to the 12th digit (including the 12th digit), substrings of length 4 are formed
    for index in range(len(credit_card)-3):
        substring = credit_card[index : index + 4]
        # Define a counter that counts the number of same back-to-back digits in any substring
        counter = 1
        for digit in range(len(substring) - 1):
            # Increase the counter by 1, if any 2 back-to-back digits in the substring are same
            # If counter reaches 4, then the credit card number is not valid
            if substring[digit] == substring[digit + 1]:
                counter += 1
                if counter == 4:
                    return False, "No 4 back-to-back digits in the credit card number can be same"

    return True


def convert_to_currency(original_currency, desired_currency, price):
    """Convert price into MKD, EUR or USD"""

    price = float(price)
    original_currency = original_currency.upper()
    desired_currency = desired_currency.upper()

    # Using an API key to request latest exchange rates from fixer.io
    # As per fixer.io's documentation, the base currency is EUR, which means that all rates are relative to EUR
    API_KEY = "13c1d8b6ad2676c9afe6e02c310457fd"

    # The provided API key is free and it provides a limited number of requests
    # In case the number of made requests exceeds the allowed number of requests, relevant data will not be provided. Therefore, the request and the parcing of data are caught in a "try - except" clause
    try:
        rate_response = requests.get(f"http://data.fixer.io/api/latest?access_key={API_KEY}")
        data = rate_response.json()
        
        rates = data["rates"]

        eur_to_mkd = rates["MKD"]
        eur_to_usd = rates["USD"]
    
    # If making the request fails for any reason (like exceeding the number of allowed requests), the exchange rates at the time of creating this program are hard coded
    except:
        eur_to_mkd = 61.63
        eur_to_usd = 1.10

    usd_to_mkd = eur_to_mkd / eur_to_usd
    usd_to_eur = 1 / eur_to_usd
    mkd_to_eur = 1 / eur_to_mkd
    mkd_to_usd = 1 / usd_to_mkd 

    # Convert price from original currency to desired currency
    if original_currency == "EUR":
        if desired_currency == "MKD":
            return price * eur_to_mkd
        else:
            return price * eur_to_usd
    elif original_currency == "USD":
        if desired_currency == "MKD":
            return price * usd_to_mkd
        else:
            return price * usd_to_eur
    else:
        if desired_currency == "EUR":
            return price * mkd_to_eur
        else:
            return price * mkd_to_usd