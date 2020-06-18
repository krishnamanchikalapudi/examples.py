"""
Session: 9
Topic: Vehicle Class
"""
class Vehicle:
    wheels = 4 # global variable inside class

    # constructor
    def __init__(self):
        print("default wheels for vehicle = {}".format(self.wheels))


v = Vehicle()
