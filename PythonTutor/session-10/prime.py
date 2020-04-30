"""
Session: 10
Topic: A positive integer greater than 1 which has no other factors except 1 and the number itself is called a prime number.
"""
num = int(input("How many terms? "))

# prime numbers are greater than 1
if num > 1:
    # check for factors
    for i in range(2, num):
        if (num % i) == 0:
            print(num, "is not a prime number")
            print(i, "times", num // i, "is", num)
            break
    else:
        print(num, "is a prime number")

# if input number is less than
# or equal to 1, it is not prime
else:
    print(num, "is not a prime number")