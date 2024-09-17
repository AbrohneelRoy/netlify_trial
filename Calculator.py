def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Cannot divide by zero."


def calculator():
    global result
    print("Simple Calculator\n")

    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Please enter valid numeric values.")
        return

    operation = input("Choose operation (+, -, *, /): ")

    if operation not in ['+', '-', '*', '/']:
        print("Invalid operation. Please choose +, -, *, or /.")
        return

    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        result = divide(num1, num2)

    print(f"\nResult: {result}")


if __name__ == "__main__":
    calculator()

