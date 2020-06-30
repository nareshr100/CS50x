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
string candidates[4] = {"a", "b", "c", "d"};
pair pairs[MAX * (MAX - 1) / 2];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

int pair_count;
int candidate_count;

// Function prototypes
void lock_pairs(void);
void print_winner(void);

int pair_count = 6;
int candidate_count = 4;

int main(void)
{
    pairs[0].winner = 3;
    pairs[0].loser = 0;
    pairs[0].margin = 5;

    pairs[1].winner = 2;
    pairs[1].loser = 1;
    pairs[1].margin = 3;

    pairs[2].winner = 0;
    pairs[2].loser = 1;
    pairs[2].margin = 1;

    pairs[3].winner =2;
    pairs[3].loser = 0;
    pairs[3].margin = 1;

    pairs[4].winner = 3;
    pairs[4].loser = 1;
    pairs[4].margin = 1;

    pairs[5].winner = 3;
    pairs[5].loser = 2;
    pairs[5].margin = 1;

    lock_pairs();
    print_winner();

}

//function for the check loops algorithm
bool check_loop_implement(int i, bool checked[])
{
    //check if already checked a candidate
    if (checked[i])
    {
        //loops exists since returned to start
        return true;
    }
    else
    {
        checked[i] = true;

        //find neighbours
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j] && check_loop_implement(j, checked))
            {
                return true;
            }
        }
    }

    return false;
}

//function to test if a path exists from one candidate to another
bool check_loop(int candidate)
{
    //create array to track which candidates have been checked via loops
    bool checked[candidate_count];

    for (int i = 0; i < candidate_count; i++)
    {
        //initialise all checked to false
        checked[i] = false;
    }

    return check_loop_implement(candidate, checked);
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    //iterate through pairs for number of pair (pair_count)
    for (int i = 0; i < pair_count; i++)
    {
        int w = pairs[i].winner;
        int l = pairs[i].loser;

        //initialise graph
        locked[w][l] = true;

        //if there are loops remove link
        if (check_loop(w))
        {
            locked[w][l] = false;
        }
    }

    for (int j = 0; j < pair_count; j++)
    {
        int a = pairs[j].winner;
        int b = pairs[j].loser;
        printf("locked[%i][%i] = %d\n", a, b,locked[a][b]);
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{
    //count no. of winners
    int n = 0;

    // find row of adjacenecy matrix with no trues
    for (int j = 0; j < candidate_count; j++)
    {
        bool winner = false;

        for (int i = 0; i < candidate_count; i++)
        {
            //printf("i,j,locked[i][j] = %i,%i,%d\n", i, j, locked[i][j]);

            if (locked[i][j])
            {
                //not winner
                winner = false;
                break;
            }
            else
            {
                winner = true;
                n++;
            }
        }

        if (winner)
        {
            printf("winner is: %s\n", candidates[j]);
        }
    }

    if (n < 1)
    {
        printf("no winner\n");
    }

    return;
}