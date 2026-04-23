def get_menu_options():
    menu = {}
    while True:
        print("Type 'Q' when done")
        category = input(
            "Please give me the category for this part of the menu: "
        ).upper()
        if category == "Q":
            break
        items = input("Please enter items separated by commas: ")
        menu[category] = items
    return menu


def save_to_file(menu):
    with open("menu.txt", "a") as file:
        all_items = menu.items()
        for item in all_items:
            output = f"{item[0]} : {item[1]}"
            file.write(output + "\n")


def main():
    my_menu = get_menu_options()
    save_to_file(my_menu)


main()
