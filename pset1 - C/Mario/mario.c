#include <cs50.h>
#include <stdio.h>

int get_positive_int(void);
void pyramid(int n);

int main(void)
{
    //Get size of pyramid from user
    int n = get_positive_int();
    //Print pyramid
    pyramid(n);
    
}

//Require positive integer from user
int get_positive_int(void)
{
    int n;
    
    do
    {
        n = get_int("How high is your pyramid?\n");
    }
    while (n < 1 || n > 8);
    return n;
}

//Function to print a single hash
void hash(int n)
{
    //print n hashes
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
}

//Function to print spaces
void space(int n)
{
    //print single space
    for (int i = 0; i < n; i++)
    {
        printf(" ");
    }
}

//Function that creates a pyramid of size n
void pyramid(int n)
{
    for (int i = 0; i < n; i++)
    {
        //spaces to centre pyramid
        space(n - i - 1);
        //pyramid structure
        hash(i + 1);
        space(2);
        hash(i + 1);
        //add new line for next pyramid level
        printf("\n");
    }
}