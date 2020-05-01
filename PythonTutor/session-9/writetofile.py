"""
Session: 9
Topic: Open & write to file
"""

import uuid

filename = 'somefile1.txt'

def writetofile():
    wToFile = open(filename, 'wt')
    uid = uuid.uuid1().int
    print('UID is {} '.format(uid))
    wToFile.writelines('Uid is {}'.format(uid))
    wToFile.close()
    print('Writing done! \n\n')

# read
def readfromfile():
    rFromFile = open(filename, 'rt')
    for line in rFromFile:
        print (line)
    rFromFile.close()
    print('reading done!')

writetofile()
readfromfile()