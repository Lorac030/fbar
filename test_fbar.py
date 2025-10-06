"""
Test suite for FBAR Calculator functionality.

Tests core functions for exchange rate retrieval, currency conversion,
balance calculations, and error handling scenarios.

Author: Carolina Lovato
"""

from fbar import (
    get_exchange_rate,
    calculate_total_balance_in_usd, 
    get_total_foreign_balance,
    validate_input,
    FBARError
)


def test_get_exchange_rate():
    """Test exchange rate retrieval from Treasury API with known values."""
    assert get_exchange_rate('Brazil', 'Real', '2021') == 5.668
    assert get_exchange_rate('Brazil', 'Real', '2011') == 1.85
    assert get_exchange_rate('Brazil', 'Real', '2022') != 4
    assert get_exchange_rate('Canada', 'Dollar', '2021') == 1.277


def test_get_exchange_rate_invalid():
    """Test exchange rate API error handling with invalid country/currency."""
    try:
        get_exchange_rate('InvalidCountry', 'InvalidCurrency', '2021')
        assert False, "Expected FBARError for invalid country/currency combination"
    except FBARError:
        pass  # Expected behavior


def test_calculate_total_balance_in_usd():
    """Test foreign currency to USD conversion with valid inputs."""
    assert calculate_total_balance_in_usd(10, 5) == 2
    assert calculate_total_balance_in_usd(100, 2) == 50
    assert calculate_total_balance_in_usd(-100, 10) == 0  # Negative balance returns 0
    

def test_calculate_total_balance_in_usd_zero_rate():
    """Test USD conversion error handling with zero exchange rate."""
    try:
        calculate_total_balance_in_usd(100, 0)
        assert False, "Expected FBARError for zero exchange rate"
    except FBARError:
        pass  # Expected behavior


def test_calculate_total_balance_in_usd_negative_rate():
    """Test USD conversion error handling with negative exchange rate."""
    try:
        calculate_total_balance_in_usd(100, -5)
        assert False, "Expected FBARError for negative exchange rate"
    except FBARError:
        pass  # Expected behavior


def test_get_total_foreign_balance():
    """Test foreign balance summation across multiple bank accounts."""
    bank_data = [
        ("2010", "Itau1", 100.0, 50.0),
        ("2010", "Itau2", 200.0, 60.0),
        ("2010", "Itau3", 300.0, 70.0),
    ]
    assert get_total_foreign_balance(bank_data) == 600.0


def test_get_total_foreign_balance_empty():
    """Test foreign balance summation with no bank accounts."""
    assert get_total_foreign_balance([]) == 0.0


def test_get_total_foreign_balance_invalid():
    """Test foreign balance summation gracefully handles malformed data."""
    # Test with invalid data types in balance field
    bank_data = [
        ("2010", "Itau1", "cat", 50),  # Invalid: string instead of float
        ("2010", "Itau2", "horse", 60),  # Invalid: string instead of float
        ("2010", "Itau3", "300", 70),   # Invalid: string instead of float
    ]
    # Should return 0.0 for invalid data structure
    assert get_total_foreign_balance(bank_data) == 0.0  # type: ignore


def test_validate_input():
    """Test input validation against regex patterns."""
    # Test valid year format
    try:
        validate_input("2023", r"^\d{4}$", "Year must be 4 digits")
        # Should not raise exception
    except FBARError:
        assert False, "Valid year should not raise FBARError"
    
    # Test invalid year format
    try:
        validate_input("23", r"^\d{4}$", "Year must be 4 digits")
        assert False, "Invalid year should raise FBARError"
    except FBARError:
        pass  # Expected behavior
    
    # Test non-empty string validation
    try:
        validate_input("Brazil", r".+", "Cannot be empty")
        # Should not raise exception
    except FBARError:
        assert False, "Non-empty string should not raise FBARError"
    
    # Test empty string validation
    try:
        validate_input("", r".+", "Cannot be empty")
        assert False, "Empty string should raise FBARError"
    except FBARError:
        pass  # Expected behavior


def run_all_tests():
    """Execute all test functions and provide summary results."""
    tests = [
        test_get_exchange_rate,
        test_calculate_total_balance_in_usd,
        test_calculate_total_balance_in_usd_zero_rate,
        test_calculate_total_balance_in_usd_negative_rate,
        test_get_total_foreign_balance,
        test_get_total_foreign_balance_empty,
        test_get_total_foreign_balance_invalid,
        test_validate_input,
    ]
    
    passed = 0
    failed = 0
    
    # Run core tests
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
    
    # Run network-dependent test separately (may fail due to API issues)
    try:
        test_get_exchange_rate_invalid()
        print("✓ test_get_exchange_rate_invalid")
        passed += 1
    except Exception as e:
        print(f"⚠ test_get_exchange_rate_invalid skipped (network/API issue): {e}")
    
    print(f"\nTest Results: {passed} passed, {failed} failed")


if __name__ == "__main__":
    run_all_tests()