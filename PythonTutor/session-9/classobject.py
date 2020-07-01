"""
Session: 9
Topic: Class
"""
class MyClass:
    x = 100 # global variable inside class

    # constructor
    def __init__(self):
        print("init X = {}".format(self.x))
        print('Class initialize')

    @classmethod
    def hello(self):
        y = 200 # global variable inside function only
        print ("hello X = {}". format(self.x))
        print("hello Y = {}".format(y))
        return 'Hello World!'

    @classmethod
    def add(self, num1, num2):
        print("add X = {}".format(self.x))
        return (num1 + num2)

    # destructor or deletes class
    def __del__(self):
        print("X = {}".format(self.x))
        print('destroy object')


c = MyClass()


# print('X is {}'.format(self.x))
print('c.X is {}'.format(c.x))
print('hello method value is {}'.format(c.hello()))
print('add method value is {}'.format(c.add(10, 20)))
