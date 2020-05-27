"""
Session: 6
Topic: Operator Precedence
"""
x = 2
y = 3



print ('x + y * x  is {} '. format(x + y * x)) # 2 + 3 * 2 = Satvika 8, Yashwant 8, Nihar 8, Nandhini 8, Mountina 8

print ('(x + y) * x  is {} '. format((x + y) * x)) # (2 + 3) * 2 =  Satvika 10, Yashwant 10, Nihar 10 , Nandhini 10, Mountina 10

print ('x + (y * x)  is {} '. format(x + (y * x)))  # 2 + (3 * 2) =  Satvika 8, Yashwant 8, Nihar 8, Nandhini 8, Mountina 8

# ( (2 + 3 ) * 2) + (3 * 2)   =  ( (5 ) * 2) + (6) =  ( 10) + (6) = 16
#  Satvika 16 , Yashwant 16, Nihar 16, Nandhini 16, Mountina 16, Sanjat 16
print ('(( (x + y ) * 2) + (y * x) )  is {} '. format(( x + y  * 2) + (y * x) ) )
