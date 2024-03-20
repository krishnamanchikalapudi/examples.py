"""
Session: 6
Topic: Boolean Operators
"""

x = ('orange', 'apple', 'pear', 'banana', 'kiwi', 'pineapple')
y = 'apple'


print (x[0])

if (y is not x[1]):
    print ('expression is false, y = {} is x = {}' .format(y, x[1]))
else:
    print('expression is true, y = {} is x = {}'. format(y, x[1]))