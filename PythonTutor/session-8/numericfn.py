"""
Session: 8
Topic: Numeric functions
"""
import math

x = '50'
y = int(x)

p = -10
q = 10.9

print ('x is {type(x)}')
print (f'x is {type(x)}')

print ('y is {type(y)}')
print (f'y is {type(y)}')

print ('the ceil of {} is {}'.format(q, math.ceil(q)))
print ('the floor of {} is {}'.format(q, math.floor(q)))
print ('absolute value of {} is {}'.format(q, math.fabs(q)))
print ('factorial of {} is {}'.format(y, math.factorial(y)))