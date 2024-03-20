"""
Session: 9
Topic: Open & write to file
"""

import uuid

rFilename = 'file.tsv'
wFilename = 'file.sql'

def parseFile():
   #  wToFile = open(wFilename, 'wt')

    with open(rFilename, 'rt') as rToFile:
        for l in rToFile:
            # print ( l.strip().split("\t") )
            lineContent = l.strip().split('\t')
            # print(type(lineContent))
            #print("length = {} ".format( len(lineContent) ))

            sqlStr = "('"
            # for x in lineContent:
            for x in range(len(lineContent)):
                sqlStr += lineContent[x]
                if (x != 2):
                    sqlStr += ("', '")
                else:
                    sqlStr += ("' ), ")

            print("{} ".format( sqlStr ))
        # wToFile.writelines(list(zip(*(line.strip().split('\t') for line in inp))))
        # wToFile.writelines(line)

    # wToFile.close()
    print('Writing done! \n\n')



parseFile()
