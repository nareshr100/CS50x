#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
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
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
            i -= 1;
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    //iterate over all candidates to find match
    for (int i = 0; i < MAX; i++)
    {
        //check if vote matches name of candidate
        string cand_name = (string) candidates[i].name;

        if ((int) cand_name == 0)
        {
            ;
        }
        else if (strcmp(name, cand_name) == 0)
        {
            //increment vote counter for candidate
            candidates[i].votes++;
            return true;
        }
    }

    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    //initialise winner at 0
    string winners[MAX];

    for (int k = 0; k < MAX; k++)
    {
        winners[k] = (string) '\0';
    }

    winners[0] = candidates[0].name;
    int max_votes = candidates[0].votes;
    string c = candidates[0].name;

    int i = 1;

    while ((int) c != 0 && i < MAX + 1)
    {
        //check if votes more than next candidate
        if (candidates[i].votes > max_votes)
        {
            //set winner to this
            winners[i] = candidates[i].name;
            winners[i - 1] = (string) '\0';
            max_votes = candidates[i].votes;
            i++;
            c = (string) candidates[i].name;

        }
        else if (candidates[i].votes == max_votes)
        {
            winners[i] = candidates[i].name;
            i++;
            c = (string) candidates[i].name;
        }
        else
        {
            i++;
            c = (string) candidates[i].name;
        }
    }

    //Print winners
    for (int j = 0; j < MAX; j++)
    {
        string w = winners[j];

        if ((int) w != 0)
        {
            printf("%s\n", candidates[j].name);
        }
    }

    return;
}