"""
Session: 9
Topic: Class
"""
class MyClass:
    x = 100

    # constructor
    def __init__(self):
        print('Class initialize')

    @classmethod
    def hello(self):
        return 'Hello World!'

    @classmethod
    def add(self, num1, num2):
        return (num1 + num2)

    # destructor or deletes class
    def __del__(self):
        print('destroy object')

c = MyClass()
print('X is {}'.format(c.x))
print('hello method value is {}'.format(c.hello()))
print('add method value is {}'.format(c.add(10, 20)))
