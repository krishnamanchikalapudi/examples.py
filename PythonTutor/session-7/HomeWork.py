"""
Session: 7
Topic: Homework - simple calculator
"""

# function adds two numbers
def add(x, y):
    return x + y

# function subtracts two numbers
def subtract(x, y):
    return x - y

# function multiplies two numbers
def multiply(x, y):
    return x * y

# function divides two numbers
def divide(x, y):
    return x / y

# decision function
def calculate(num1, num2, choice):
    if choice == '1':
        val = add(num1, num2)
        print('num1 + num2 = {}'.format(val) )

    elif choice == '2':
        val = subtract(num1, num2)
        print('num1 - num2 = {}'.format( val) )

    elif choice == '3':
        val = multiply(num1, num2)
        print('num1 * num2 = {}'.format( val) )

    elif choice == '4':
        val = divide(num1, num2)
        print('num1 / num2 = {}'.format( val) )
    else:
        print('Invalid input!')

print('Select operation.\n\t {} \n\t {} \n\t {} \n\t {} '. format('1.Add', '2.Subtract', '3.Multiply', '4.Divide'))
oper = input("Enter choice(1/2/3/4): ") # Take input from the user

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

calculate(num1, num2, oper)