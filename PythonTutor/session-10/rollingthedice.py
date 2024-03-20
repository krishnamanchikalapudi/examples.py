import random
"""
Session: 10
Topic: Rolling the dice
"""

min = 1
max = 6

roll_again = "yes"

while roll_again == "yes" or roll_again == "y":
    print ('Rolling the dices...')
    print ('Dice 1 is {}'.format(random.randint(min, max)))
    print ('Dice 2 is {}'.format(random.randint(min, max)))

    roll_again = input("Roll the dices again? ")