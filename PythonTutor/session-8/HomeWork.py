import platform
"""
Session: 9
Topic: iterate SET & List
"""
myset = {'orange', 'apple', 'pear', 'banana', 'kiwi', 'pineapple', 'apple'}
mylist = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'pineapple', 'apple']


print ('myset length is {}'.format(len(myset)))

i=0
for val in myset:
    print ('\tFOR:: myset of {} is {}'.format(i, val))
    i += 1


print ('\n mylist length is {}'.format(len(mylist)))
i=0
while i < len(mylist):
    print ('\tWHILE:: mylist of {} is {}'.format(i, mylist[i]))
    i += 1
print ('\n')
for i in range(len(mylist)):
    print ('\tFOR:: mylist of {} is {}'.format(i, mylist[i]))