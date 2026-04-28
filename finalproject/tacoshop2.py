# GLOBAL CONSTANTS (Pantry Rules)
MENU_FILE = "menu.txt"


def get_customer_info():
    """Asks for name and Table number with validation."""
    name = input("Customer Name: ").title()

    while True:
        location = input("Table Number: ")
        if location.isdigit():
            break
        print("Invalid input. Table number must be numbers only.")

    return name, location


def read_menu():
    menus = {}

    try:
        with open("menu.txt", "r") as file:
            for line in file:
                # FIX: your file uses ":" not ";"
                parts = [p.strip() for p in line.split(":")]
                category = parts[0].upper()
                detail = parts[1]
                menus[category] = detail
        return menus
    except Exception as e:
        print(e)
        return {}


def create_variables(menu_items):
    # FIX: convert comma-separated strings into lists
    tortilla = [t.strip().title() for t in menu_items.get("TORTILLA").split(",")]
    meat = [m.strip().title() for m in menu_items.get("MEAT").split(",")]
    toppings = [t.strip().title() for t in menu_items.get("TOPPINGS").split(",")]
    categories = [c.strip().title() for c in menu_items.get("CATEGORY").split(",")]

    return tortilla, meat, toppings, categories


def take_order(tortilla_options, meat_options, toppings, categories):
    """Collects taco category, tortilla, protein, and extras with validation."""

    # CATEGORY
    print("Category Options:", ", ".join(categories))
    while True:
        category = input("Choose category: ").title()
        if category in categories:
            break
        print("Invalid choice. Please choose a valid category.")

    # TORTILLA (only for Taco)
    if category == "Taco":
        print("Tortilla Options:", ", ".join(tortilla_options))
        while True:
            tortilla = input("Choose tortilla: ").title()
            if tortilla in tortilla_options:
                break
            print("Invalid choice. Please choose a valid tortilla.")
    else:
        tortilla = "N/A"

    # PROTEIN
    print("Protein Options:")
    for m in meat_options:
        print(m)

    while True:
        protein = input("Choose protein: ").title()
        if protein in meat_options:
            break
        print(f"Invalid choice. Please choose from {meat_options}")

    # EXTRAS
    print("Extras Options:", ", ".join(toppings))
    while True:
        extras = input("Extras (comma separated, optional): ").strip()

        if extras == "":
            extras_list = []
            break

        raw_list = [e.strip().title() for e in extras.split(",")]

        if all(e in toppings for e in raw_list):
            extras_list = raw_list
            break
        else:
            print("Invalid topping detected. Try again.")

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
    extra_cost = 0.25

    base = category_prices.get(order_data["category"], 3.00)
    protein_cost = protein_upcharge.get(order_data["protein"], 0)
    extras_total = len(order_data["extras"]) * extra_cost

    return base + protein_cost + extras_total


def save_data_and_label(customer, location, total, order_data):
    """Appends to order_history.txt and prints the human-readable label."""

    print("--- KITCHEN TICKET ---")
    print(f"TABLE NUMBER: {location} | NAME: {customer}")
    print(f"ITEM: {order_data['category']}")
    print(f"TORTILLA: {order_data['tortilla']}")
    print(f"PROTEIN: {order_data['protein']}")
    print(
        f"EXTRAS: {', '.join(order_data['extras']) if order_data['extras'] else 'None'}"
    )
    print(f"TOTAL: ${total:.2f}")

    with open("order_history.txt", "a") as file:
        file.write(
            f"{customer},{location},{order_data['category']},"
            f"{order_data['tortilla']},{order_data['protein']},"
            f"{'|'.join(order_data['extras']) if order_data['extras'] else 'None'},"
            f"{total:.2f}\n"
        )


def main():
    name, location = get_customer_info()

    menus = read_menu()

    tortilla, meat, toppings, category = create_variables(menus)

    current_order = take_order(tortilla, meat, toppings, category)

    final_price = calculate_total(current_order)

    save_data_and_label(
        customer=name, location=location, total=final_price, order_data=current_order
    )


main()
