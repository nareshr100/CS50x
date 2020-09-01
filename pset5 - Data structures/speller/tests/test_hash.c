#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include "dictionary.h"

unsigned int hash(const char *word);

// Number of buckets in hash table
const unsigned int N = 26;

int main(void)
{
    const char word[5] = {'h', 'e', 'l', 'l', 'o'};
    /*word[0] = 'h';
    word[1] = 'e';
    word[2] = 'l';
    word[3] = 'l';
    word[4] = 'o';*/

    printf("wordhash = %i\n", hash(word));
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //load first letter of word and make hash value
    unsigned int wordhash = (int) word[0];
    printf("%i\n", wordhash);

    if (wordhash > 64 && wordhash < 91)
    {
        wordhash -= 65;
    }
    else if (wordhash > 96 && wordhash < 123)
    {
        wordhash -= 97;
    }
    else
    {
        printf("error finding hash value of %s\n", word);
    }

    //ensure less than N
    wordhash %= N;

    return wordhash;
}