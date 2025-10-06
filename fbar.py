# project.py
# Carolina Lovato

import requests
import tabulate
import sys
import re
import datetime


# Get exchange rate from Treasury website API
def get_exchange_rate(country_name, currency_name, year):
    try:
        # API address
        url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange"
        # aditional parameters for the API
        params = {
            "format": "json",
            "fields": "exchange_rate,record_date",
            "filter": f"country_currency_desc:in:(USA-Dollar,{country_name}-{currency_name}),record_date:eq:{year}-12-31"
        }
        # uses the requests library to get something from the API
        response = requests.get(url, params=params)
        # from response, gets the json, extracts first element of data, then extracts exchange_rate
        _usd_rate = float(response.json().get('data')[0].get('exchange_rate'))
    except IndexError:
        print("\nUnfortunatelly this call to Treasury system returned no data. Typically what happens is that this combination of Country and Currency is not supported for the year you requested.")
        sys.exit(1)
    except Exception as e:
        # prints a message and exits when anything goes wrong with trying to use the API
        print("\nSomething went wrong with your request, please check input values and try again")
        sys.exit(1)
    return _usd_rate


# calculates total balance in US dollars
def calculate_total_balance_in_USD(total_balance, exchange_rate):
    # exchange rate cannot be zero
    if exchange_rate == 0:
        return None
    # total balance must be bigger than zero
    if total_balance > 0:
        # makes the calculation
        return total_balance / exchange_rate
    else:
        return 0


# sums all values in foreign currency
# bank_data = []
#  0: year
#  1: bank name
#  2: foreign balance
#  3: USD balance
def get_total_foreign_balance(bank_data):
    try:
        result = 0
        # for each item inside the list...
        for item in bank_data:
            # gets index 2 of the list and adds it to result
            result += item[2]
        return result
    except:
        # if anything goes wrong returns 0
        return 0


# generic function to validate inputs based on patterns
def validate_input(value, pattern):
    if not re.match(pattern, value):
        print("Value not acceptable")
        sys.exit(1)


# calculates fbar from user input
def main():
    print("-----------------------------")
    print("FBAR Calculator")
    print("-----------------------------")
    print()

    # gets year from user
    current_year = datetime.datetime.now().year
    default_year = str(current_year - 1)
    year = input(f"Tax Return Year (like {default_year}): ") or default_year
    # only accepts four-digits year
    validate_input(year,r"^\d\d\d\d$")
    # gets name of the country from user
    country_name = input("Country of where your assets are (like Brazil): ") or "Brazil"
    # at least one letter or digit
    validate_input(country_name,r".+")
    # gets name of currency from user
    currency_name = input(f"Currency Name for {country_name} (like Real): ") or "Real"
    # at least one letter or digit
    validate_input(currency_name,r".+")
    # gets symbol of currency from user
    currency_symbol = input("Currency Symbol for that country (like R$): ") or "R$"
    # validates if symbol has 1 letter at least
    validate_input(currency_symbol,r".+")

    # gets dollar value for requested parameters (Dec 31st for the year)
    usd_rate = get_exchange_rate(country_name, currency_name, year)

    # ask for bank names and balances
    bank_data = []
    print()
    # loop to request all bank names and balances
    while True:
        # asks user for a bank name
        bank_name = input("Enter bank name (leave blank to finish): ")
        if not bank_name:
            break
        # bank name cannot be empty
        validate_input(bank_name,r".+")
        # asks user for the balance 
        balance = input(f"- Enter highest balance on {year} in {currency_symbol} for {bank_name}: ")
        # balance can only be number(s)
        validate_input(balance,r"^[0-9]+$")
        # converts balance into float
        balance = float(balance)
        # puts every input inside an "item", then inside a list
        bank_data.append([year, bank_name, balance, calculate_total_balance_in_USD(balance, usd_rate)])

    # extracts total foreing balance from bank data
    total_foreign_balance = get_total_foreign_balance(bank_data)
    # converts foreign balance into US dollar
    total_balance_in_USD = calculate_total_balance_in_USD(total_foreign_balance, usd_rate)
    # prints summary of user input without values
    print(f"\nDolar to {currency_name} Treasury reference for {year} is {currency_symbol}{usd_rate}")
    print()
    # bank data needs to have more than one entry to...
    if len(bank_data) > 0:
        # define the table header and...
        header = ['Year', 'Bank Name', 'Currency in ' + currency_symbol, 'Currency in US$']
        # prints the table
        print(tabulate.tabulate(bank_data, header, tablefmt="grid", floatfmt=".2f"))
        print()
    print(f"Total balance of {currency_symbol}{total_foreign_balance:.2f} on {year} was equivalent to US${total_balance_in_USD:.2f}")
    if total_balance_in_USD >= 10000:
        # prints a message (fbar needed) since total balance is >= 10000
        print(f"As it exceeds US$10,000 you MAY NEED to file an FBAR form on April of {int(year)+1}.")
        print("Please go to https://bsaefiling.fincen.treas.gov/NoRegFBARFiler.html and type all asset values there for online FBAR filing.")
    else:
        # prints a message (fbar NOT needed) since total balance is < 10000
        print(f"As it does not exceed US$10,000 you may not need to file a FBAR form on April of {int(year)+1}.")


if __name__ == "__main__":
    main()
