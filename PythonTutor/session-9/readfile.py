"""
Session: 9
Topic: Open & read file
"""

def readfromfile():
    f = open('somefile.txt')
    for line in f:
        print (line)
    f.close
    print('Good bye!')

readfromfile()