#include <cs50.h>
#include <stdio.h>
#include <math.h>

long long get_card_number(void);
int digit(long long n, int d);
int length(long long n);
long long power(int base, int power);
int luhn(long long n);
void classify_card_number(long long n);

int main(void)
{
    //Get credit card number from user input prompt
    long long n = get_card_number();
    //Classify card based on user input
    classify_card_number(n);
}

//Function to find number of digits in a number
int length(long long n)
{
    //initialise variables
    int l = 0;
    
    // Find length by repeatedly dividing by 10
    if (n == 0)
    {
        l = 1;
    }
    else
    {
        while (n != 0)
        {
            n /= 10;
            l++;
        }
    }

    return l;
}

//Function to ensure user input is of the right form for a card number
long long get_card_number(void)
{
    //initialise variables
    long long n;

    //Get user input for card
    n = get_long_long("What is your card number?\n");

    return n;
}

//Functio to find power of a number
long long power(int base, int power)
{
    //initialise variable
    long long result = base;
    
    if (power == 0)
    {
        result = 1;
    }
    else
    {
        for (int i = 0; i < (power - 1); i++)
        {
            result *= base;
        }
    }
    
    return result;
}

//Function to find specific digit of a number
int digit(long long n, int d)
{
    //initialise variables
    long long digit1 = 0;
    int digit = 0;
    long long p1 = 0;
    long long p2 = 0;
    
    //Cut number such that most significant digit is the required one
    p1 = power(10, d);
    digit1 = n % p1;
    
    //Remove trailing digits unless d=1
    if (d == 1)
    {
        ;
    }
    else
    {
        p2 = power(10, d - 1);
        digit1 /= p2;
    }
    
    digit = digit1;
    
    return digit;
}

//Function to calculate the result of Luhn's Algoithm
int luhn(long long n)
{
    //initialise variables
    int d = 0;
    int luhn1 = 0;
    int luhn2 = 0;
    int luhn = 0;
    
    //Find sum of digits of every other digit starting from second last multiplied by 2
    for (int i = 2; i < length(n) + 2; i += 2)
    {
        //Find every other digit starting from second to last
        d = digit(n, i);
        //Multiply individual digits by 2
        d *= 2;
        
        
        for (int j = 1; j <= length(d); j++)
        {
            //Add digits of twice the alternate digits to sum1
            luhn1 += digit(d, j);
        }
        
        //Find sum of digits of remaining digits in same iteration and add to sum2
        luhn2 += digit(n, i - 1);
    }
    
    //Find sum of the two individual sums
    luhn = luhn1 + luhn2;

    return luhn;
}

//Function to classify a card number by company
void classify_card_number(long long n)
{
    //Initialise variables to perform logic functions
    int lu = luhn(n);
    int l = length(n);
    int digit_last = digit(lu, 1);
    int digit1 = digit(n, length(n));
    int digit2 = digit(n, (length(n) - 1));
    
    if (digit_last != 0  ||  l < 13  ||  l > 16)
    {
        printf("INVALID\n");
    }
    else if ((digit1 == 3  &&  digit2 == 4)  || (digit1 == 3  &&  digit2 == 7))
    {
        printf("AMEX\n");
    }
    else if (digit1 == 5  && (digit2 > 0  &&  digit2 < 6))
    {
        printf("MASTERCARD\n");
    }
    else if (digit1 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}