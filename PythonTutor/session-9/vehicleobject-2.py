"""
Session: 9
Topic: Vehicle Class
"""
class Vehicle:
    wheels = 4 # global variable inside class

    # constructor
    def __init__(self):
        print("default wheels for Vehicle = {}".format(self.wheels))

    @classmethod
    def fn(self, num1, num2):
        return (num1 + num2)



v = Vehicle()
print("Vehicle function value is {} ".format( v.fn(10, 20) ))
