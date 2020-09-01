from cs50 import get_int


def main():

    # prompt user for input
    n = get_int("How high is your pyramid\n")

    # re-prompt if not in required range
    while (n <= 0 or n > 8):
        n = get_int("That height is invalid.\n")

    # run pyramid function
    pyramid(n)


# function to print pyramid with n levels
def pyramid(n):

    for i in range(n):
        
        # perform for each level in pyramid
        print((n - i - 1) * " ", end="")
        print((i + 1) * "#", end="")
        print(2 * " ", end="")
        print((i + 1) * "#")


main()