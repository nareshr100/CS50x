#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Get *name* from user
    string name = get_string("What is your name?\n");
    
    //Print "hello, *name*"
    printf("hello, %s\n", name);
}