from datetime import date


def normalize_registration(plate):
    """
    Removes spaces, dashes and dots from a registration number and upper-cases it.
    Returns an empty string for None or non-string input.
    """
    if not isinstance(plate, str):
        return ""
    plate = "".join(plate.split())          # removes all whitespace types
    for ch in ['-', '.']:
        plate = plate.replace(ch, '')
    return plate.upper()


def total_claim_amount(text):
    """
    Adds up claim amounts separated by semicolons.
    Empty, non-numeric and negative entries are ignored.
    Returns 0 for None or non-string input.
    """
    if not isinstance(text, str):
        return 0
    total = 0
    for amount in text.split(';'):
        try:
            value = int(amount.strip())
        except ValueError:
            continue                         # skip junk like "", "abc", "1.5"
        if value >= 0:
            total += value
    return total


def driver_age(dob, current_year=2026):
    """
    Works out the driver's age from a DD/MM/YYYY date of birth.
    Returns None if the input is not a valid date or is in the future.
    """
    if not isinstance(dob, str):
        return None
    parts = dob.strip().split('/')
    if len(parts) != 3:
        return None
    try:
        day, month, year = (int(p) for p in parts)
        date(year, month, day)               # validates day/month/year ranges
    except (ValueError, OverflowError):
        return None
    age = current_year - year
    return age if age >= 0 else None

def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    age = driver_age(value)
    print("Driver age in 2026:", age if age is not None else "Invalid date of birth")

if __name__ == "__main__":
    main()
