#include <cs50.h>
#include <stdio.h>
#include <string.h>

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

//function to merge two arrays of pairs from highest to lowest
void merge(pair array[], int s, int m, int e)
{
    //initialise variables
    int l1 = m-s+1;
    int l2 = e - m;

    //create temporary arrays for max number of pairs - 36 with 9 candidates
    pair array1[18], array2[18];

    //fill temporary arrays
    for (int i = 0; i < l1; i++)
    {
        array1[i].winner = array[s+i].winner;
        array1[i].loser = array[s+i].loser;
        array1[i].margin = array[s+i].margin;
    }

    for (int j = 0; j < l2; j++)
    {
        array2[j].winner = array[m+j+1].winner;
        array2[j].loser = array[m+j+1].loser;
        array2[j].margin = array[m+j+1].margin;
    }

    //reset iterative counters
    int i = 0;
    int j = 0;

    //combine arrays based on which element is larger
    for(int k = s; k <= e; k++)
    {
        if(array1[i].margin >= array2[j].margin)
        {
            array[k].winner = array1[i].winner;
            array[k].loser = array1[i].loser;
            array[k].margin = array1[i].margin;
            i++;
        }
        else
        {
            array[k].winner = array2[j].winner;
            array[k].loser = array2[j].loser;
            array[k].margin = array2[j].margin;
            j++;
        }
    }

    return;
}

//function to mergesort array
void mergesort(pair pairs_array[], int s, int e)
{
    //initialise variables
    int m;

    //check if mergesort is incomplete
    if(s < e)
    {
        //calculate midpoint
        m = (s + e)/2;

        // break up into halves
        mergesort(pairs_array, s, m);
        mergesort(pairs_array, m + 1, e);

        //merge two arrays and repeat
        merge(pairs_array, s, m, e);
    }

  return;
}


// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    //find number of votes who prefer i over j, maybe use mergesort to sort?
    //recursion?
    for (int i = 0; i < pair_count; i++)
    {
        printf("pair winner: %i\n", pairs[i].winner);
        printf("pair loser: %i\n", pairs[i].loser);
        printf("pair margin: %i\n", pairs[i].margin);
    }

    mergesort(pairs, 0, pair_count - 1);

    for (int j = 0; j < pair_count; j++)
    {
        printf("sorted pair winner: %i\n", pairs[j].winner);
        printf("sorted pair loser: %i\n", pairs[j].loser);
        printf("sorted pair margin: %i\n", pairs[j].margin);
    }

    return;
}
