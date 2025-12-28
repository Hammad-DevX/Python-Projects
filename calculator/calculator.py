def get_float_number(prompt: str) -> float:
    while True:
        try: 
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_number(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt))
            if 1 <= num <= 5:
                return num
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def add(num1: float, num2: float) -> float:
    return num1 + num2

def subtract(num1: float, num2: float) -> float:
    return num1 - num2

def multiply(num1: float, num2: float) -> float:
    return num1 * num2

def divide(num1: float, num2: float) -> float:
    if num2 == 0:
        raise ZeroDivisionError("Cannot Divide By Zero")
    return num1 / num2

        

first_number = get_float_number("Enter First Number: ")


while True:
    print("=== Smart Calculator ===")

    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    operation_choice = get_int_number("Enter Your Choice Between (1 - 5): ")

    if operation_choice == 5:
        print("Byeee")
        break

    second_number = get_float_number("Enter Next Number: ")
    try:
        match operation_choice:
            case 1: result = add(first_number, second_number)
            case 2: result = subtract(first_number, second_number)
            case 3: result = multiply(first_number, second_number)
            case 4: result = divide(first_number, second_number)
    except ZeroDivisionError as e:
        print(e)
        continue

    first_number = result

    print(f"Updated Result: {first_number}")




