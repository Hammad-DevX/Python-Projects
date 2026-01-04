
contact_dictionary = {}

def get_int(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt))
            if 1 <= num <= 5:
                return num
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Enter a number.")


def add_contact():

    # Get and validate name
    name = input("Enter valid name: ").strip().lower()

    if not name:
        print("Name cannot be empty.")
        return

    if name in contact_dictionary:
        print("Contact already exists.")
        return
    
    while True:
        phone_number = input("Enter phone number: ").strip()

        # Optional: validate only digits
        if not phone_number.isdigit():
            print("Phone number must contain only digits.")
            continue

        # Optional: length check (example: 7–15 digits)
        if not (7 <= len(str(phone_number)) <= 15):
            print("Phone number length is invalid.")
            continue

        phone_set = set(contact_dictionary.values())

        if phone_number in phone_set:
            print("Phone number already exists.")
            continue

        contact_dictionary[name] = phone_number
        print("Successfully added.")
        break

def view_contact():
    if not contact_dictionary:
        print("No contacts to Display.")
        return

    # Column headers
    name_header = "Name"
    phone_header = "Phone Number"

    max_name_len = max(len(name_header),
                        max(len(name) for name in contact_dictionary))
    max_phone_len = max(len(phone_header), 
                                max(len(str(phone_number)) for phone_number in contact_dictionary.values()))

    # Total width of the rectangle
    total_width = max_name_len + max_phone_len + 7

    # Top border
    print("*" * total_width)

    # Header row
    print(
        f"* {name_header:<{max_name_len}} | "
        f"{phone_header:<{max_phone_len}} *"
    )

    # Separator
    print("*" * total_width)

    # Data rows
    for name, phone in contact_dictionary.items():
        print(
            f"* {name:<{max_name_len}} | "
            f"{phone:<{max_phone_len}} *"
        )

    # Bottom border
    print("*" * total_width)

def search_contact():
    if not contact_dictionary:
        print("No contacts to search.")
        return

    name = input("Enter name: ").strip().lower()

    if not name:
        print("Name cannot be empty.")
        return


    phone = contact_dictionary.get(name)
    
    if phone is None:
        print("Contact not found.")
    else:
        print(f"Name : {name}")
        print(f"Phone: {phone}")


def delete_contact():
    if not contact_dictionary:
        print("No contacts to Delete.")
        return
    
    name = input("Enter name: ").strip().lower()
    if not name:
        print("Name cannot be empty.")
        return
    
    phone = contact_dictionary.pop(name, None)
    
    if phone is None:
        print("Contact not found.")
    else:
        print(f"Name : {name}")
        print(f"Phone: {phone}")
        print("Deleted successfully.")

def menu():

    while True:
        print("=== Contact Book ===")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Exit")
        
        choice = get_int("Enter Your Choice:")

        match choice:
            case 1:
                add_contact()
            case 2:
                view_contact()
            case 3:
                search_contact()
            case 4:
                delete_contact()
            case 5:
                print("Good bye")
                break
            case _:
                print("Please re-ernter value between (1-5)")


menu()

