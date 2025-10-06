"""
FBAR Calculator - Foreign Bank Account Report compliance tool.

This module calculates whether US taxpayers need to file FBAR forms based on 
foreign bank account balances and official Treasury exchange rates.

Author: Carolina Lovato
"""

import datetime
import re
import sys
from typing import List, Tuple

import requests
import tabulate


# Constants
FBAR_THRESHOLD = 10000.0
API_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange"


class FBARError(Exception):
    """Custom exception for FBAR-related errors."""
    pass


def get_exchange_rate(country_name: str, currency_name: str, year: str) -> float:
    """Retrieve official Treasury exchange rate for foreign currency to USD.
    
    Fetches the December 31st exchange rate from the US Treasury fiscal service API
    for the specified country, currency, and year combination.
    
    Args:
        country_name: Name of the country (e.g., 'Brazil')
        currency_name: Name of the currency (e.g., 'Real') 
        year: Four-digit year as string (e.g., '2021')
        
    Returns:
        Exchange rate as float (foreign currency units per 1 USD)
        
    Raises:
        FBARError: If API call fails, returns no data, or country/currency combination 
                  is not supported for the requested year
    """
    try:
        # Build API request parameters
        params = {
            "format": "json",
            "fields": "exchange_rate,record_date",
            "filter": f"country_currency_desc:in:(USA-Dollar,{country_name}-{currency_name}),record_date:eq:{year}-12-31"
        }
        
        # Make API request
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        # Parse response data
        data = response.json().get('data', [])
        if not data:
            raise FBARError(
                f"\nNo exchange rate data found for {country_name}-{currency_name} in {year}. "
                "This combination may not be supported for the requested year."
            )
            
        return float(data[0]['exchange_rate'])
        
    except (requests.RequestException, KeyError, ValueError, IndexError) as e:
        raise FBARError(
            f"\nFailed to retrieve exchange rate data. Please check your input values and try again."
        ) from e


def calculate_total_balance_in_usd(total_balance: float, exchange_rate: float) -> float:
    """Convert foreign currency balance to US dollars using official exchange rate.
    
    Args:
        total_balance: Balance in foreign currency units
        exchange_rate: Official Treasury exchange rate (foreign currency units per 1 USD)
        
    Returns:
        Balance converted to USD (minimum value of 0.0)
        
    Raises:
        FBARError: If exchange rate is zero or negative
    """
    if exchange_rate <= 0:
        raise FBARError("Exchange rate must be positive")
        
    return max(0, total_balance / exchange_rate)


def get_total_foreign_balance(bank_data: List[Tuple[str, str, float, float]]) -> float:
    """Calculate total foreign currency balance across all bank accounts.
    
    Safely sums the foreign currency balances (third element) from all bank 
    account tuples, handling invalid data gracefully.
    
    Args:
        bank_data: List of tuples containing (year, bank_name, foreign_balance, usd_balance)
        
    Returns:
        Total foreign currency balance, or 0.0 if data is invalid/empty
    """
    try:
        return sum(item[2] for item in bank_data)
    except (IndexError, TypeError, ValueError):
        return 0.0


def validate_input(value: str, pattern: str, error_message: str) -> None:
    """Validate user input against a regular expression pattern.
    
    Args:
        value: Input string to validate
        pattern: Regular expression pattern for validation
        error_message: Human-readable error message for validation failures
        
    Raises:
        FBARError: If input doesn't match the specified pattern
    """
    if not re.match(pattern, value):
        raise FBARError(f"Invalid input: {error_message}")


def get_user_input() -> Tuple[str, str, str, str]:
    """Collect and validate all required user input for FBAR calculation.
    
    Prompts user for tax year, country, currency name, and currency symbol with
    sensible defaults and input validation.
    
    Returns:
        Tuple of (year, country_name, currency_name, currency_symbol)
        
    Raises:
        FBARError: If any input validation fails
    """
    current_year = datetime.datetime.now().year
    default_year = str(current_year - 1)
    
    year = input(f"Tax Return Year (like {default_year}): ") or default_year
    validate_input(year, r"^\d{4}$", "Year must be 4 digits")
    
    country_name = input("Country of where your assets are (like Brazil): ") or "Brazil"
    validate_input(country_name, r".+", "Country name cannot be empty")
    
    currency_name = input(f"Currency Name for {country_name} (like Real): ") or "Real"
    validate_input(currency_name, r".+", "Currency name cannot be empty")
    
    currency_symbol = input("Currency Symbol for that country (like R$): ") or "R$"
    validate_input(currency_symbol, r".+", "Currency symbol cannot be empty")
    
    return year, country_name, currency_name, currency_symbol


def get_bank_data(year: str, currency_symbol: str, exchange_rate: float) -> List[Tuple[str, str, float, float]]:
    """Interactively collect bank account data from user input.
    
    Prompts user to enter bank names and their highest balances for the tax year,
    automatically converting to USD using the provided exchange rate.
    
    Args:
        year: Four-digit tax year as string
        currency_symbol: Display symbol for the foreign currency (e.g., 'R$')
        exchange_rate: Official Treasury exchange rate for USD conversion
        
    Returns:
        List of tuples containing (year, bank_name, foreign_balance, usd_balance)
        
    Raises:
        FBARError: If bank name or balance validation fails
    """
    bank_data = []
    print()
    
    while True:
        bank_name = input("Enter bank name (leave blank to finish): ")
        if not bank_name:
            break
            
        validate_input(bank_name, r".+", "Bank name cannot be empty")
        
        balance_input = input(f"- Enter highest balance on {year} in {currency_symbol} for {bank_name}: ")
        validate_input(balance_input, r"^[0-9]+$", "Balance must be a positive number")
        
        balance = float(balance_input)
        usd_balance = calculate_total_balance_in_usd(balance, exchange_rate)
        
        bank_data.append((year, bank_name, balance, usd_balance))
    
    return bank_data


def display_results(
    bank_data: List[Tuple[str, str, float, float]], 
    year: str, 
    currency_name: str, 
    currency_symbol: str, 
    exchange_rate: float
) -> None:
    """Display formatted results table and FBAR filing requirements.
    
    Shows exchange rate, bank account details in a formatted table, total balances,
    and determines whether FBAR filing is required based on the $10,000 threshold.
    
    Args:
        bank_data: List of tuples containing (year, bank_name, foreign_balance, usd_balance)
        year: Four-digit tax year as string
        currency_name: Full name of the foreign currency (e.g., 'Real')
        currency_symbol: Display symbol for the foreign currency (e.g., 'R$')
        exchange_rate: Official Treasury exchange rate used for conversion
    """
    total_foreign_balance = get_total_foreign_balance(bank_data)
    total_usd_balance = calculate_total_balance_in_usd(total_foreign_balance, exchange_rate)
    
    print(f"\nDollar to {currency_name} Treasury reference for {year} is {currency_symbol}{exchange_rate}")
    print()
    
    if bank_data:
        headers = ['Year', 'Bank Name', f'Currency in {currency_symbol}', 'Currency in US$']
        print(tabulate.tabulate(bank_data, headers, tablefmt="grid", floatfmt=".2f"))
        print()
    
    print(f"Total balance of {currency_symbol}{total_foreign_balance:.2f} on {year} was equivalent to US${total_usd_balance:.2f}")
    
    if total_usd_balance >= FBAR_THRESHOLD:
        print(f"As it exceeds US${FBAR_THRESHOLD:,.0f} you MAY NEED to file an FBAR form on April of {int(year)+1}.")
        print("Please go to https://bsaefiling.fincen.treas.gov/NoRegFBARFiler.html and type all asset values there for online FBAR filing.")
    else:
        print(f"As it does not exceed US${FBAR_THRESHOLD:,.0f} you may not need to file a FBAR form on April of {int(year)+1}.")


def main() -> None:
    """Main entry point for FBAR calculator application.
    
    Orchestrates the complete FBAR calculation workflow: user input collection,
    exchange rate retrieval, bank data gathering, and results display.
    """
    print("-----------------------------")
    print("FBAR Calculator")
    print("-----------------------------")
    print()
    
    try:
        # Collect user input
        year, country_name, currency_name, currency_symbol = get_user_input()
        
        # Fetch official Treasury exchange rate
        exchange_rate = get_exchange_rate(country_name, currency_name, year)
        
        # Gather bank account data
        bank_data = get_bank_data(year, currency_symbol, exchange_rate)
        
        # Calculate and display results
        display_results(bank_data, year, currency_name, currency_symbol, exchange_rate)
        
    except FBARError as e:
        print(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()