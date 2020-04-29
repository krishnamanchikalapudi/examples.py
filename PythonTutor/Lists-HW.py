"""
Home work
1. Create new project 'HomeWork-3"
2. Create file 'HW.py'
3. Create List variable 'fruits' with values: orange, apple, pear, banana, kiwi
3.1. print the size or count of list. Tip: len(fruits)
3.2. add new fruit 'grapes' to list 'fruits', print the size of list. Tip: fruits.append("grapes")
3.3. remove fruit 'apple' from list 'fruits', print the size of list. Tip: fruits.remove('apple')
3.4. reverse the list values and print the list. Tip: fruits.reverse()
"""

fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']

print ("list size = ", len(fruits) )

print ("count of apples = ", fruits.count('apple'))

fruits.append("grapes")
print ('list size is ', len(fruits), ' has ', fruits)

fruits.remove('apple')
print ("list size = ", len(fruits) )
print ("list has ", fruits)


fruits.reverse()
print ("list size = ", len(fruits) )
print ("list has ", fruits)