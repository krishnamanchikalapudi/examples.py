"""
Session: 7
Topic: Function returns
"""

p = 10

def calculator (num1, num2, oper):
    q= 20
    print (p)
    print(q)
    if (oper == "+"):
        print(p)
        print (q)
        return add(num1, num2)

def add(num1, num2):
    print(p)
    # print(q)
    num = (num1 + num2)
    print (num)
    return num



# print ('5 + 10 = {} '. format( calculator(5, 10, "+") ) )

addv = add(10, 20)
print ('10 + 20 = {} '. format( addv ) )
print(p)