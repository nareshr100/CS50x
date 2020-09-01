import numpy as np
from cs50 import get_int


def main():

    # Get credit card number from user input prompt
    n = get_card_number()

    # Classify card based on user input
    classify_card_number(n)


# Function to find number of digits in a number
def length(n):

    l = int(0)

    if (n == 0):

        l = 1

    else:

        while (n != 0):

            n = int(n // 10)
            l += 1

    return l

# function to ensure user input is of the right form for a card number


def get_card_number():

    # Get user input for card
    n = get_int("What is your card number?\n")

    return n
    

def power(base, power):

    # initialise variable
    result = base

    if (power == 0):

        result = 1

    else:

        for i in range(power - 1):

            result *= base
            i += 1

    return result


def digit(n, d):

    # initialise variables
    digit1 = int(0)
    digit = int(0)
    p1 = int(0)
    p2 = int(0)

    # Cut number such that most significant digit is the required one
    p1 = power(10, d)
    digit1 = int(n) % p1

    # Remove trailing digits unless d=1
    if (d != 1):

        p2 = power(10, d - 1)
        digit1 = int(digit1 / p2)

    digit = digit1

    return digit


def luhn(n):

    # initialise variables
    d = int(0)
    luhn1 = int(0)
    luhn2 = int(0)
    luhn = int(0)

    # Find sum of digits of every other digit starting from second last multiplied by 2
    for i in range(2, (length(n) + 2), 2):

        # Find every other digit starting from second to last
        d = digit(n, i)

        # Multiply individual digits by 2
        d *= 2

        for j in range(1, (length(d) + 1)):

            # Add digits of twice the alternate digits to sum1
            luhn1 += digit(d, j)

        # Find sum of digits of remaining digits in same iteration and add to sum2
        luhn2 += digit(n, i - 1)

    # Find sum of the two individual sums
    luhn = int(luhn1 + luhn2)

    return luhn

def classify_card_number(n):

    # Initialise variables to perform logic functions
    lu = luhn(n)
    l = length(n)
    digit_last = digit(lu, 1)
    digit1 = digit(n, length(n))
    digit2 = digit(n, (length(n) - 1))

    if (digit_last != 0 or l < 13 or  l > 16):

        print("INVALID")

    elif ((digit1 == 3 and digit2 == 4) or (digit1 == 3 and digit2 == 7)):

        print("AMEX")

    elif (digit1 == 5 and (digit2 > 0 and digit2 < 6)):

        print("MASTERCARD")

    elif (digit1 == 4):

        print("VISA")

    else:

        print("INVALID")


main()