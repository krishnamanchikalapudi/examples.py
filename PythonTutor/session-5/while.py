"""
Session: 5
Topic: While loop
"""

fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'pineapple', 'cherry']

count = 0
while (count < len(fruits)):
    print ('count at {} fruit is {}'.format(count, fruits[count]))
    count = (count + 1)
    if (count == 3):
        break
    # count += 1



print("size / 2 = {}".format(len(fruits)/2))

print("number of fruits in array {}".format(len(fruits)))
print ('Good bye!')