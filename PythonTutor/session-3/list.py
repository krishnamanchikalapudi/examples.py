"""
Session: 3
Topic: Array or List
"""
fruits = ['apple', 'banana', 'carrot']

print ('number of fruits in basket {}'. format( len(fruits)))
print (fruits)

print ('second fruit in basket is {}'. format( fruits[2]))

# add fruit
fruits.append('orange')
print ('number of fruits in basket {}'. format( len(fruits)))
print (fruits)

# remove fruit
fruits.remove('banana')
print ('number of fruits in basket {}'. format( len(fruits)))
print (fruits)

# reverse list
fruits.reverse()
print ('number of fruits in basket {}'. format( len(fruits)))
print (fruits)