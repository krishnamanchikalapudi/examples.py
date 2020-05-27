"""
Session: 5
Topic: for loop
"""

fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'pineapple']

for i in fruits:
    print (i)

print("number of fruits in array {}".format(len(fruits)))


print ('\n\n')
for i in range (len(fruits)):
    if (i == 3):
        break
    print ('fruit at {} is {}'. format(i, fruits[i]))
