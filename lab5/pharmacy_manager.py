"""Pharmacy stock and billing manager.

Adds medicines, dispenses them, flags expired stock, bills prescriptions,
computes dosages, saves stock to a JSON file and checks a pharmacist login.
"""
import ast
import hashlib
import json
import operator
import os
import secrets
from datetime import date, datetime

# Global pharmacy state (mutated in place, never rebound)
MEDICINES = {}
DB_PASSWORD = os.environ.get("PHARMACY_PASSWORD")

# Safe arithmetic evaluator (replaces eval)
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add stock for a medicine and return the audit log list."""
    if audit is None:
        audit = []
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Invalid medicine name: {name!r}")
    if qty < 0:
        raise ValueError(f"Quantity cannot be negative: {qty}")
    if name not in MEDICINES:
        MEDICINES[name] = {"qty": 0, "price": price, "expiry": expiry}
    MEDICINES[name]["qty"] += qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit


def dispense_medicine(name, qty):
    """Remove qty units of a medicine; raise ValueError if not possible."""
    if name not in MEDICINES:
        raise ValueError(f"{name} is not in stock")
    if qty > MEDICINES[name]["qty"]:
        raise ValueError(f"Insufficient stock for {name}")
    MEDICINES[name]["qty"] -= qty


def get_quantity(name):
    """Return the quantity in stock for a medicine."""
    return MEDICINES[name]["qty"]


def is_expired(name):
    """Return True if the medicine's expiry date has passed."""
    exp = datetime.strptime(MEDICINES[name]["expiry"], "%Y-%m-%d").date()
    return exp < date.today()


def bill_amount(prescription):
    """Return the total bill; refuse to bill expired medicines."""
    total = 0
    for medicine, count in prescription:
        if is_expired(medicine):
            raise ValueError(f"{medicine} is expired and cannot be billed")
        total += MEDICINES[medicine]["price"] * count
    return total


def _eval_node(node):
    """Recursively evaluate a parsed arithmetic expression."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        op_func = _OPS[type(node.op)]
        return op_func(_eval_node(node.left), _eval_node(node.right))
    raise ValueError("Invalid dosage formula")


def calculate_dosage(formula):
    """Evaluate a dosage formula such as '250 * 2' safely."""
    return _eval_node(ast.parse(formula, mode="eval"))


def patient_id(name, phone):
    """Return a SHA-256 based patient identifier."""
    return hashlib.sha256((name + phone).encode()).hexdigest()


def generate_rx_number():
    """Return a random prescription number."""
    return "RX-" + str(secrets.randbelow(900000) + 100000)


def save_stock(file="pharmacy.json"):
    """Save the stock to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(MEDICINES, handle)


def load_stock(file="pharmacy.json"):
    """Load the stock from a JSON file."""
    with open(file, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    MEDICINES.clear()
    MEDICINES.update(data)


def print_label(name):
    """Print a dispensing label."""
    print("Dispensing label:", name)


def expiring_soon(days=30):
    """Return medicines expiring within the given number of days."""
    result = []
    for name, info in MEDICINES.items():
        exp = datetime.strptime(info["expiry"], "%Y-%m-%d").date()
        if (exp - date.today()).days < days:
            result.append(name)
    return result


def pharmacist_login(password):
    """Check the password against the PHARMACY_PASSWORD env variable."""
    return bool(DB_PASSWORD) and password == DB_PASSWORD


def print_stock():
    """Print the stock report."""
    print("===== Pharmacy Stock Report =====")
    for name, info in MEDICINES.items():
        print(name, "->", info["qty"], "units, Rs.", info["price"],
              "exp", info["expiry"])


def main():
    """Run a short demo."""
    audit = add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15", audit)
    for bad_args in (("Cetirizine 10mg", -10, 2.0, "2027-03-31"), (404, 25)):
        try:
            add_medicine(*bad_args)
        except ValueError as err:
            print("Rejected:", err)
    for name, qty in (("Paracetamol 500mg", 30), ("Insulin", 2)):
        try:
            dispense_medicine(name, qty)
        except ValueError as err:
            print("Cannot dispense:", err)
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount([("Paracetamol 500mg", 10)]))
    try:
        bill_amount([("Amoxicillin 250mg", 5)])
    except ValueError as err:
        print("Billing refused:", err)
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login("pharma@123"))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()