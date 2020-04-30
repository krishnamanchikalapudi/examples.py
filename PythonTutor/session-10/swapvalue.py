"""
Session: 10
Topic: swap two variables by using a temporary variable and, without using temporary variable
"""
x = 5
y = 10

# create a temporary variable and swap the values
temp = x
x = y
y = temp
print('x after swapping: {}'.format(x))
print('y after swapping: {}'.format(y))

# without temp variable
p = 5
q = 10
p, q = q, p
print('\np after swapping: {}'.format(p))
print('q after swapping: {}'.format(q))