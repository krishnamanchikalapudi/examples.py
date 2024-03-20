"""
Session: 9
Topic: Open & read file
"""

def readfromfile():
    f = open('../session-10/somefile-1.txt')
    for line in f:
        print (line)
    f.close
    print('Good bye!')

readfromfile()