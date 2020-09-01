// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

int main(void)
{
    const char word[5] = {'h', 'e', 'l', 'l', 'o'};


    //allocate memory for node
    node *n = malloc(sizeof(node));

    if (n == NULL)
    {
        return 1;
    }

    //copy word and insert into node n
    strcpy(n->word, word);

    table[7] = n;
    n->next = NULL;

    printf("%s\n", table[7]->word);

    printf("wordhash = %i\n", hash(word));
    printf("check = %d\n", check(word));

    return 0;
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

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //find hash value of first letter in word
    unsigned int wordhash = hash(word);

    //go to this location of hash table and check linked list
    node *tmp = table[wordhash];

    while (tmp != NULL)
    {
        printf("%s\n", (*tmp).word);

        printf("%d\n", strcasecmp((*tmp).word, word));

        //check if word is stored here
        if (strcasecmp((*tmp).word, word) == 0)
        {
            return true;
        }
        else
        {
            //update temp to view next node in linked list
            tmp = tmp->next;
        }
    }

    return false;
}