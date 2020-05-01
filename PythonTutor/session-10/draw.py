import turtle
"""
Session: 10
Topic: Turtle is a Python feature like a drawing board, which lets us command a turtle to draw all over it!
"""

# Initializing the turtle
t = turtle.Turtle()

""" 
# draw Square
s = 100
for _ in range(4):
  t.forward(s) # Forward turtle by s units
  t.left(90) # Turn turtle by 90 degree
"""

# draw rectangle
l = 300
w = 150
# drawing first side
t.forward(l)  # Forward turtle by l units
t.left(90)  # Turn turtle by 90 degree

# drawing second side
t.forward(w)  # Forward turtle by w units
t.left(90)  # Turn turtle by 90 degree

# drawing third side
t.forward(l)  # Forward turtle by l units
t.left(90)  # Turn turtle by 90 degree

# drawing fourth side
t.forward(w)  # Forward turtle by w units
t.left(90)  # Turn turtle by 90 degree

"""
# circle drawing
r = 50
t.circle(r)
"""

"""
# tangent circle drawing
r = 10 # radius for smallest circle
n = 10 # number of circles

for i in range(1, n + 1, 1):  # loop for printing tangent circles
    t.circle(r * i)
"""

"""   
# spiral circle drawing
r = 10  # taking radius of initial radius

for i in range(100):    # Loop for printing spiral circle
    t.circle(r + i, 45)
"""

"""    
# concentric circle drawing

r = 10  # radius of the circle 
for i in range(50):  # Loop for printing concentric circles
    t.circle(r * i)
    t.up()
    t.sety((r * i)*(-1))
    t.down()
"""