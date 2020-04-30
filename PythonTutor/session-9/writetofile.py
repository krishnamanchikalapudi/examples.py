"""
Session: 9
Topic: Open & write to file
"""

import uuid

filename = 'somefile1.txt'
writeToFile = open(filename, 'wt')
uid = uuid.uuid1().int
print('UID is {} '.format(uid))
writeToFile.writelines('Uid is {}'.format(uid))
writeToFile.close()

print('Writing done! \n\n')

# read
readFromFile = open(filename, 'rt')
for line in readFromFile:
    print (line)
readFromFile.close()

print('reading done!')