"""
Session: 5
Topic: While loop
"""

fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'pineapple']

count = 0
while (count < len(fruits)):
    print ('count at {} fruit is {}'.format(count, fruits[count]))
    count = (count + 1)
    # count += 1

print ('Good bye!')