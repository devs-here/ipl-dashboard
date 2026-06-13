class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        self.result = a + b
        return self.result

    def subtract(self, a, b):
        self.result = a - b
        return self.result

    def multiply(self, a, b):
        self.result = a * b
        return self.result

    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero"
        self.result = a / b
        return self.result

    def display(self):
        print(f"Result: {self.result}")


# Main program
calc = Calculator()

while True:
    print("\n1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "5":
        print("Goodbye!")
        break

    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    if choice == "1":
        calc.display() if False else print(f"Result: {calc.add(a, b)}")
    elif choice == "2":
        print(f"Result: {calc.subtract(a, b)}")
    elif choice == "3":
        print(f"Result: {calc.multiply(a, b)}")
    elif choice == "4":
        print(f"Result: {calc.divide(a, b)}")
    else:
        print("Invalid choice!")