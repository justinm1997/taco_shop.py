"""
ASSIGNMENT 10B: SPRINT 3 - REFACTORING & DATA ACCOUNTABILITY
Project: Taco Shop (V3.0)
Developer: Justin Moravec
"""

import datetime

# GLOBAL CONSTANTS
MENU_FILE = "menu.txt"
DATA_FILE = "order_history.txt"
HUMAN_REPORT = "human_report.txt"

TORTILLA_OPTIONS = ("Corn", "Flour")
MEAT_OPTIONS = ("Chicken", "Beef", "Steak")
TOPPING_OPTIONS = ("Lettuce", "Tomato", "Cheese", "Onion", "Salsa")


def get_customer_info():
    """Asks for name and Table number."""
    name = input("Customer Name: ").title()
    location = input("Table Number: ")
    return name, location


def take_order():
    """Collects taco category, tortilla, protein, and extras."""

    print("\n--- MENU OPTIONS ---")
    print("Category: Taco / Burrito / Nachos")
    print(f"Tortillas: {TORTILLA_OPTIONS}")
    print(f"Proteins: {MEAT_OPTIONS}")
    print(f"Extras: {TOPPING_OPTIONS}")

    category = input("\nChoose category: ").title()
    tortilla = input("Choose tortilla: ").title()
    protein = input("Choose protein: ").title()

    extras = input("Extras (comma separated): ")
    extras_list = [e.strip().title() for e in extras.split(",")] if extras else []

    return {
        "category": category,
        "tortilla": tortilla,
        "protein": protein,
        "extras": extras_list,
    }


def calculate_total(order_data):
    """Calculates price based on category, protein, and extras."""

    category_prices = {"Taco": 3.00, "Burrito": 8.00, "Nachos": 10.00}
    protein_upcharge = {"Beef": 1.00, "Chicken": 1.00, "Steak": 2.00}
    extra_cost = 0.50

    base = category_prices.get(order_data["category"], 3.00)
    protein_cost = protein_upcharge.get(order_data["protein"], 0)
    extras_total = len(order_data["extras"]) * extra_cost

    return base + protein_cost + extras_total


def save_data_and_label(customer, location, total, order_data):
    """Saves raw data and writes a human-readable ticket."""

    # Append raw data
    with open(DATA_FILE, "a") as f:
        f.write(f"{customer},{location},{total:.2f}\n")

    # Human-readable ticket
    with open(HUMAN_REPORT, "w") as f:
        f.write(f"TACO SHOP TICKET - {datetime.date.today()}\n")
        f.write(f"TABLE: {location} | NAME: {customer}\n")
        f.write(f"ITEM: {order_data['category']}\n")
        f.write(f"TORTILLA: {order_data['tortilla']}\n")
        f.write(f"PROTEIN: {order_data['protein']}\n")
        f.write(
            f"EXTRAS: {', '.join(order_data['extras']) if order_data['extras'] else 'None'}\n"
        )
        f.write(f"TOTAL: ${total:.2f}\n")


def main():
    name, location = get_customer_info()
    current_order = take_order()
    final_price = calculate_total(current_order)
    save_data_and_label(
        customer=name, location=location, total=final_price, order_data=current_order
    )
    print(f"\n✅ Files Updated: {DATA_FILE} and {HUMAN_REPORT}")


main()
