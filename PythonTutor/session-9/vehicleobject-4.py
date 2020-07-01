"""
Session: 9
Topic: Vehicle Class

Overloading allows different methods to have the same name, but different signatures where the signature can differ by the number of input parameters or type of input parameters or both
"""
class Vehicle:
    wheels = 4 # global variable inside class

    # constructor
    def __init__(self):
        print("default wheels for Vehicle = {}".format(self.wheels))

    @classmethod
    def fn(self, num1, num2):
        return (num1 + num2)


"""
Topic: Car inherits Vehicle Class
"""
class Car(Vehicle):
    wheels = 3
    def __init__(self):
        print("default wheels for Car = {} and Vehicle = {} ".format(self.wheels, super().wheels))

    @classmethod
    def fn(self, num1, num2):
        return (num1 * num2)


c = Car()
print("Car function value is {} ".format( c.fn(10, 20) ))

v = Vehicle()
print("Vehicle function value is {} ".format( v.fn(10, 20) ))
