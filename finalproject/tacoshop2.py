# GLOBAL CONSTANTS (Pantry Rules)
MENU_FILE = "menu.txt"
# TORTILLA_OPTIONS = ("Corn", "Flour")
# MEAT_OPTIONS = ("Chicken", "Beef", "Steak")
# TOPPING_OPTIONS = ("Lettuce", "Cilantro", "Tomato", "Cheese", "Onion", "Salsa")
# CATEGORY_OPTIONS = ("Taco", "Burrito", "Nachos")


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
    def read_menu():
        menus = {}

    try:
        with open("menu.txt", "r") as file:
            for line in file:
                parts_of_line = line.strip().split(";")
                category = parts_of_line[0].strip()
                detail = parts_of_line[1].strip()
                menus[category] = detail
        return menus
    except Exception as e:
        print(e)


def create_variables(menu_items):  # menus is a dictionary

    tortilla = menu_items.get("TORTILLA")
    meat = menu_items.get("MEAT")
    toppings = menu_items.get("TOPPINGS")
    categories = menu_items.get("CATEGORY")

    return tortilla, meat, toppings, categories


def take_order(tortilla, meat, toppings, categories):
    """Collects taco category, tortilla, protein, and extras with validation."""

    # CATEGORY
    print("Category Options: Taco / Burrito / Nachos")
    while True:
        category = input("Choose category: ").title()
        if category in categories:
            break
        print("Invalid choice. Please choose Taco, Burrito, or Nachos.")

    # TORTILLA (only for Taco)
    if category == "Taco":
        print("Tortilla Options: Flour / Corn")
        while True:
            tortilla = input("Choose tortilla: ").title()
            if tortilla in tortilla:
                break
            print("Invalid choice. Please choose Flour or Corn.")
    else:
        tortilla = "N/A"

    # PROTEIN
    print("Protein Options:")
    for meat in meat:
        print(meat)

    while True:
        protein = input("Choose protein: ").title()
        if protein in meat:
            break
        print(f"Invalid choice. Please choose {meat}")

    # EXTRAS (validation)
    print("Extras Options: Lettuce, Tomato, Cheese, Onion, Salsa")
    while True:
        extras = input("Extras (comma separated, optional): ").strip()

        # Allow empty input (no extras)
        if extras == "":
            extras_list = []
            break

        # Process list
        raw_list = [e.strip().title() for e in extras.split(",")]

        # Validate all extras
        if all(e in toppings for e in raw_list):
            extras_list = raw_list
            break
        else:
            print("Invalid topping detected. Please enter only valid toppings.")
            print("Valid options: Lettuce, Cilantro, Tomato, Cheese,\ Onion, Salsa")

    return {
        "category": category,
        "tortilla": tortilla,
        "protein": protein,
        "extras": extras_list,
    }


def calculate_total(order_data):
    """Calculates price based on category, protein, and extras."""

    # Base prices by category
    category_prices = {"Taco": 3.00, "Burrito": 8.00, "Nachos": 10.00}

    # Protein upcharges
    protein_upcharge = {"Beef": 1.00, "Chicken": 1.00, "Steak": 2.00}

    # Extras cost (each)
    extra_cost = 0.25

    # Determine base price
    base = category_prices.get(order_data["category"], 3.00)

    # Add protein cost
    protein_cost = protein_upcharge.get(order_data["protein"], 0)

    # Add extras cost
    extras_total = len(order_data["extras"]) * extra_cost

    return base + protein_cost + extras_total


def save_data_and_label(customer, location, total, order_data):
    """Appends to order_history.txt and prints the human-readable label."""

    # Print ticket
    print("--- KITCHEN TICKET ---")
    print(f"TABLE NUMBER: {location} | NAME: {customer}")
    print(f"ITEM: {order_data['category']}")
    print(f"TORTILLA: {order_data['tortilla']}")
    print(f"PROTEIN: {order_data['protein']}")
    # source citation
    print(
        f"EXTRAS: {', '.join(order_data['extras']) if order_data['extras'] else 'None'}"
    )
    print(f"TOTAL: ${total:.2f}")

    # Save to file
    with open("order_history.txt", "a") as file:
        file.write(
            f"{customer},{location},{order_data['category']},"
            f"{order_data['tortilla']},{order_data['protein']},"
            f"{'|'.join(order_data['extras']) if order_data['extras'] else 'None'},"
            f"{total:.2f}\n"
        )


def main():
    # 1. Identity
    name, location = get_customer_info()

    # 1B. read menu!
    menus = read_menu()

    # 1C. create variables
    tortilla, meat, toppings, category = create_variables(menus)

    # 2. Data Collection
    current_order = take_order(tortilla, meat, toppings, category)

    # 3. Calculation
    final_price = calculate_total(current_order)

    # 4. Handoff
    save_data_and_label(
        customer=name, location=location, total=final_price, order_data=current_order
    )


main()
