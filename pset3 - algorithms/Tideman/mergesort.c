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

//function to merge two arrays of pairs from highest to lowest
void merge(pair array[], int margin_array[], int s, int m, int e)
{
    //initialise variables
    int l1 = m-s+1;
    int l2 = e - m;

    //create temporary arrays for max number of pairs - 36 with 9 candidates
    pair array1[18], array2[18];
    int margins1[18], margins2[18];

    //fill temporary arrays
    for (int i = 0; i < l1; i++)
    {
        array1[i].winner = array[s+i].winner;
        array1[i].loser = array[s+i].loser;
        margins1[i] = margin_array[s+i];
    }

    for (int j = 0; j < l2; j++)
    {
        array2[j].winner = array[m+j+1].winner;
        array2[j].loser = array[m+j+1].loser;
        margins2[j] = margin_array[m+j+1];
    }

    //reset iterative counters
    int i = 0;
    int j = 0;

    //combine arrays based on which element is larger
    for(int k = s; k <= e; k++)
    {
        if(margins1[i] >= margins2[j])
        {
            array[k].winner = array1[i].winner;
            array[k].loser = array1[i].loser;
            margin_array[k] = margins1[i];
            i++;
        }
        else
        {
            array[k].winner = array2[j].winner;
            array[k].loser = array2[j].loser;
            margin_array[k] = margins2[j];
            j++;
        }
    }

    return;
}

//function to mergesort array
void mergesort(pair pairs_array[], int margin_array[], int s, int e)
{
    //initialise variables
    int m;

    //check if mergesort is incomplete
    if(s < e)
    {
        //calculate midpoint
        m = (s + e)/2;

        // break up into halves
        mergesort(pairs_array, margin_array, s, m);
        mergesort(pairs_array, margin_array, m + 1, e);

        //merge two arrays and repeat
        merge(pairs_array, margin_array, s, m, e);
    }

  return;
}


// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int *margins = get_margins();

    //find number of votes who prefer i over j, maybe use mergesort to sort?
    //recursion?
    for (int i = 0; i < pair_count; i++)
    {
        printf("pair winner: %i\n", pairs[i].winner);
        printf("pair loser: %i\n", pairs[i].loser);
        printf("pair margin: %i\n", margins[i]);
    }

    mergesort(pairs, margins, 0, pair_count - 1);

    for (int j = 0; j < pair_count; j++)
    {
        printf("sorted pair winner: %i\n", pairs[j].winner);
        printf("sorted pair loser: %i\n", pairs[j].loser);
        printf("sorted pair margin: %i\n", margins[j]);
    }

    return;
}
