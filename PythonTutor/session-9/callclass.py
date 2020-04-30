"""
Session: 9
Topic: read Class object information
"""
from .classobject import MyClass

c = MyClass()
print('X is {}'.format(c.x))
print('hello method value is {}'.format(c.hello()))
print('add method value is {}'.format(c.add(10, 20)))