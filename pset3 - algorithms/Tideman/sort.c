#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
    int margin;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count = 6;
int candidate_count = 4;

void sort_pairs(void);

int main(void)
{
    pairs[0].winner = 0;
    pairs[0].loser = 1;
    pairs[0].margin = 1;

    pairs[1].winner = 2;
    pairs[1].loser = 0;
    pairs[1].margin = 1;

    pairs[2].winner = 2;
    pairs[2].loser = 1;
    pairs[2].margin = 3;

    pairs[3].winner = 3;
    pairs[3].loser = 0;
    pairs[3].margin = 5;

    pairs[4].winner = 3;
    pairs[4].loser = 1;
    pairs[4].margin = 1;

    pairs[5].winner = 3;
    pairs[5].loser = 2;
    pairs[5].margin = 1;

    sort_pairs();
}

int cmpfunc(const void * a, const void * b)
{
    pair p1 = *((pair*) a);
    pair p2 = *((pair*) b);

    return p2.margin - p1.margin;
}

void sort_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        printf("pair winner: %i\n", pairs[i].winner);
        printf("pair loser: %i\n", pairs[i].loser);
        printf("pair margin: %i\n", pairs[i].margin);
    }

    qsort(pairs, pair_count, sizeof(pair), cmpfunc);

    for (int j = 0; j < pair_count; j++)
    {
        printf("sorted pair winner: %i\n", pairs[j].winner);
        printf("sorted pair loser: %i\n", pairs[j].loser);
        printf("sorted pair margin: %i\n", pairs[j].margin);
    }

    return;
}