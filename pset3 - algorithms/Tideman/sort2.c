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
    preferences[0][0] = 0;
    preferences[0][1] = 3;
    preferences[0][2] = 2;
    preferences[0][3] = 0;
    preferences[1][0] = 2;
    preferences[1][1] = 0;
    preferences[1][2] = 1;
    preferences[1][3] = 2;
    preferences[2][0] = 3;
    preferences[2][1] = 4;
    preferences[2][2] = 0;
    preferences[2][3] = 2;
    preferences[3][0] = 5;
    preferences[3][1] = 3;
    preferences[3][2] = 3;
    preferences[3][3] = 0;

    pairs[0].winner = 0;
    pairs[0].loser = 1;

    pairs[1].winner = 2;
    pairs[1].loser = 0;

    pairs[2].winner = 2;
    pairs[2].loser = 1;

    pairs[3].winner = 3;
    pairs[3].loser = 0;

    pairs[4].winner = 3;
    pairs[4].loser = 1;

    pairs[5].winner = 3;
    pairs[5].loser = 2;

    sort_pairs();
}

//function to get array of margins between two candidates
int * get_margins(void)
{
    static int margins[6];

    int p = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            int m = preferences[i][j] - preferences[j][i];

            if ( i != j && m > 0)
            {
                margins[p++] = m;
            }
        }
    }

    return margins;
}

int cmpfunc(const void * a, const void * b)
{
    pair p1 = *((pair*) a);
    pair p2 = *((pair*) b);

    int m1 = preferences[p1.winner][p1.loser] - preferences[p1.loser][p1.winner];
    int m2 = preferences[p2.winner][p2.loser] - preferences[p2.loser][p2.winner];

    return m2 - m1;
}

void sort_pairs(void)
{
    int *margins = get_margins();

    for (int i = 0; i < pair_count; i++)
    {
        printf("pair winner: %i\n", pairs[i].winner);
        printf("pair loser: %i\n", pairs[i].loser);
        printf("pair margin: %i\n", margins[i]);
    }

    qsort(pairs, pair_count, sizeof(pair), cmpfunc);

    for (int j = 0; j < pair_count; j++)
    {
        printf("sorted pair winner: %i\n", pairs[j].winner);
        printf("sorted pair loser: %i\n", pairs[j].loser);
        printf("sorted pair margin: %i\n", margins[j]);
    }

    return;
}