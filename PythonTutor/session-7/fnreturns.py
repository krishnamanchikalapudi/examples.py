"""
Session: 7
Topic: Function returns
"""

def calculator (num1, num2, oper):
    if (oper == "+"):
       return add(num1, num2)

def add(num1, num2):
    num = (num1 + num2)
    print (num)
    # return num


# print ('5 + 10 = {} '. format( calculator(5, 10, "+") ) )

addv = add(10, 20)
print ('10 + 20 = {} '. format( addv ) )
