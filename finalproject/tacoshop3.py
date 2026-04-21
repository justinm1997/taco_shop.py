"""
ASSIGNMENT 11B: SPRINT 4 - WRITING TO FILES
Project: taco shop (V5.0)
Developer: Justin Moravec
"""

import datetime


def write_receipt(order_dict, customer_name):
    """Takes order details and appends them to a persistent receipt log."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("store_receipts.txt", "a") as file:
        file.write(f"\n[{current_time}] ORDER: {customer_name}\n")

        for item, qty in order_dict.items():
            file.write(f" - {item}: {qty}\n")

        file.write("----------------------\n")

    print("Receipt successfully logged to system!")


def main():
    current_order = {}
    customer = input("Enter customer name: ")

    while True:
        item = input("Enter drink name (or 'done' to finish): ")
        if item.lower() == "done":
            break

        qty = input(f"How many {item}s? ")
        current_order[item] = qty

    write_receipt(current_order, customer)


main()
