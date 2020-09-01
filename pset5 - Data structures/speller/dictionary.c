// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
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

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //find hash value of first letter in word
    unsigned int wordhash = hash(word);

    //go to this location of hash table and check linked list
    node *tmp = table[wordhash];

    while (tmp != NULL)
    {
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

//-----------------------------------------------------------------------------
// MurmurHash2, by Austin Appleby

// Note - This code makes a few assumptions about how your machine behaves -

// 1. We can read a 4-byte value from any address without crashing
// 2. sizeof(int) == 4

// And it has a few limitations -

// 1. It will not work incrementally.
// 2. It will not produce the same results on little-endian and big-endian
//    machines.

unsigned int MurmurHash2(const void *key, int len, unsigned int seed)
{
    // 'm' and 'r' are mixing constants generated offline.
    // They're not really 'magic', they just happen to work well.

    const unsigned int m = 0x5bd1e995;
    const int r = 24;

    // Initialize the hash to a 'random' value

    unsigned int h = seed ^ len;

    // Mix 4 bytes at a time into the hash

    const unsigned char *data = (const unsigned char *)key;

    while (len >= 4)
    {
        unsigned int k = *(unsigned int *)data;

        k *= m;
        k ^= k >> r;
        k *= m;

        h *= m;
        h ^= k;

        data += 4;
        len -= 4;
    }

    // Handle the last few bytes of the input array

    switch (len)
    {
        case 3:
            h ^= data[2] << 16;
        case 2:
            h ^= data[1] << 8;
        case 1:
            h ^= data[0];
            h *= m;
    };

    // Do a few final mixes of the hash to ensure the last few
    // bytes are well-incorporated.

    h ^= h >> 13;
    h *= m;
    h ^= h >> 15;

    return h;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //load first letter of word and make hash value
    unsigned int wordhash = *word;
    wordhash = tolower(wordhash);

    if (wordhash > 96 && wordhash < 123)
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

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open dictionary file
    FILE *dict = fopen(dictionary, "r");

    if (dict == NULL)
    {
        printf("Could not open dictionary\n");
        return false;
    }

    //array to store word for node
    char word[LENGTH + 1];

    //read strings from file one at a time
    while (fscanf(dict, "%s", word) != EOF)
    {
        //create new node for each word
        //allocate memory for node
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            fclose(dict);
            free(n);
            return false;
        }

        //copy word and insert into node n
        strcpy(n->word, word);

        //hash word to obtain hash value
        int wordhash = hash(word);

        //insert node into hash table at this location
        //check if root of linked list is at bucket location
        if (table[wordhash] == NULL)
        {
            //node is empty so initialise linked list
            table[wordhash] = n;

            //sent pointer of root node to NULL
            n->next = NULL;
        }
        else
        {
            //linked list in bucket already initialised
            //point node at start of linked list
            n->next = table[wordhash];

            //point root to new node
            table[wordhash] = n;
        }

    }

    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int counter = 0;

    //create dummy hash table
    node *table_tmp[N];

    for (int i = 0; i < N; i++)
    {

        table_tmp[i] = table[i];

        while (table_tmp[i] != NULL)
        {
            counter++;
            table_tmp[i] = table_tmp[i]->next;
        }
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    for (int i = 0; i < N; i++)
    {
        //unload linked list at bucket location
        node *cursor = table[i];

        //create tmp pointer to store node's address
        node *tmp = cursor;

        while (cursor != NULL)
        {
            //point cursor at next node
            cursor = cursor->next;

            free(tmp);

            //point tmp at next node
            tmp = cursor;
        }

        free(tmp);
        free(cursor);
    }

    return true;
}
