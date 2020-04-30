"""
Session: 9
Topic: Open & read file
"""

f = open('somefile.txt')
for line in f:
    print (line)
f.close

print('Good bye!')
