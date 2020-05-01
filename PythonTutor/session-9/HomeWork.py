import platform
"""
Session: 9
Topic: Homework - simple calculator
"""

class SimpleCalculator:
    # constructor
    def __init__(self):
        print('Class initialize')

    # function adds two numbers
    def add(self, x, y):
        return x + y

    # function subtracts two numbers
    def subtract(self, x, y):
        return x - y

    # function multiplies two numbers
    def multiply(self, x, y):
        return x * y

    # function divides two numbers
    def divide(self, x, y):
        return x / y

    # decision function
    def calculate(self, num1, num2, choice):
        if choice == '1':
            val = self.add(num1, num2)
            print('num1 + num2 = {}'.format(val) )

        elif choice == '2':
            val = self.subtract(num1, num2)
            print('num1 - num2 = {}'.format( val) )

        elif choice == '3':
            val = self.multiply(num1, num2)
            print('num1 * num2 = {}'.format( val) )

        elif choice == '4':
            val = self.divide(num1, num2)
            print('num1 / num2 = {}'.format( val) )
        else:
            print('Invalid input!')


print('Python version is {}\n\n'.format(platform.python_version()))
sc = SimpleCalculator()
print('Select operation.\n\t {} \n\t {} \n\t {} \n\t {} '. format('1.Add', '2.Subtract', '3.Multiply', '4.Divide'))
oper = input("Enter choice(1/2/3/4): ") # Take input from the user

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

sc.calculate(num1, num2, oper)