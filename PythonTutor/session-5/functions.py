"""
Session: 5
Topic: functions
"""

def calculator(num1, num2, operator):
    if ('-' == operator ):
        print('{} {} {} = {} '.format(num1, operator, num2, (num1 - num2) ) )

    print("Good bye!")
# done calc


# function calling
calculator(10, 20, '+')
calculator(100, 20, '-')