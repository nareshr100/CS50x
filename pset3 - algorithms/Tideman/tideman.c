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

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs and initialise preferences
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
            preferences[i][j] = 0;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    //iterate over all candidates to find match
    for (int i = 0; i < MAX; i++)
    {
        //check if vote matches name of candidate
        string cand_name = candidates[i];

        if ((int) cand_name == 0)
        {
            ;
        }
        else if (strcmp(name, cand_name) == 0)
        {
            //update ranks
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

//function to find rank of candidate in ranks
int find_rank(int ranks[], int candidate)
{
    int rank_i = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        //find rank of i candidate in ranks
        if (ranks[i] == candidate)
        {
            rank_i = i;
            break;
        }
    }

    return rank_i;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    //iterate over all pairs of candidates
    //i is candidate 1
    for (int i = 0; i < candidate_count; i++)
    {
        //find rank of candidate i
        int rank_i = find_rank(ranks, i);

        //iterate to find pair and check preference
        //j is candidate 2
        for (int j = 0; j < candidate_count; j++)
        {
            //find rank of candidate j
            int rank_j = find_rank(ranks, j);

            //ignore if candidate i is candidate j
            if (i == j)
            {
                ;
            }
            //check if candidate i beats j
            else if (rank_i < rank_j)
            {
                //if preference then increment relevant preference
                preferences[i][j]++;
                printf("preference of %i over %i = %i\n", i, j, preferences[i][j]);
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    //iterate through preferences to find non zero entries
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            //ignore test versus self
            if (i == j)
            {
                //skip
                ;
            }
            //test if non zero
            else if (preferences[i][j] > preferences[j][i])
            {
                //if non zero add to pairs
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                printf("winner = %i\n", pairs[pair_count].winner);
                printf("loser = %i\n", pairs[pair_count].loser);
                pair_count++;
            }
        }
    }

    return;
}

//function to get array of margins between two candidates
int *get_margins(void)
{
    static int margins[6];

    int p = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            int m = preferences[i][j] - preferences[j][i];

            if (i != j && m > 0)
            {
                margins[p++] = m;
            }
        }
    }

    return margins;
}

int cmpfunc(const void *a, const void *b)
{
    pair p1 = *((pair *) a);
    pair p2 = *((pair *) b);

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
        printf("locked[%i][%i] = %d\n", a, b, locked[a][b]);
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