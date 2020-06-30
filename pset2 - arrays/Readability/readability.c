#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

string get_text(void);
int sentences(string text);
void classify(string text);

int main(void)
{
    //Get text from user
    string text = get_text();
    
    //Print grade level using Coleman-Liau index
    classify(text);
}

//function to get text from user
string get_text(void)
{
    string text = get_string("Text: ");
    
    //Keep asking for text until character entered
    while (strlen(text) < 1 || ((int) text[0] < 65 || ((int) text[0] > 90 && (int) text[0] < 97) || (int) text[0] > 122))
    {
        text = get_string("Text: ");
    }
    
    return text;
}
//function to find number of letters in a string (omits punctuation or spaces)
int letters(string text)
{
    //initialise variable to count letters
    int letters = 0;
    
    //iterate until end of string
    for (int i = 0; i < strlen(text); i++)
    {
        //cast individual character into decimal integer according to ASCII
        int c = (int) text[i];
        
        //check if integer value corresponds to upper/lowercase letter
        if ((c > 64 && c < 91) || (c > 96 && c < 123))
        {
            //if letter add one to counter
            letters++;
        }
        else
        {
            //if not a letter do nothing
            ;
        }
    }
    
    return letters;
}

int words(string text)
{
    //initialise variable to count words
    int words = 1;
    
    //iterate until end of string
    for (int i = 0; i < strlen(text); i++)
    {
        //cast individual character into decimal integer according to ASCII
        int c = (int) text[i];
        
        //check if integer value corresponds to space
        if (c == 32)
        {
            //if space add one to counter
            words++;
        }
        else
        {
            //if not a space do nothing
            ;
        }
    }
    
    return words;
}

//function to determine number of sentences ignoring full stops in special cases eg 'Mr.'
int sentences(string text)
{
    //initialise variable to count sentences
    int sentences = 0;
    
    //iterate until end of string
    for (int i = 0; i < strlen(text); i++)
    {
        //cast individual character into decimal integer according to ASCII
        int c = (int) text[i];
        
        //check if integer value corresponds to full stop or question or exclamation marks
        if (c == 46 || c == 33 || c == 63)
        {
            //if space add one to counter
            sentences++;
        }
        else
        {
            //if not a space do nothing
            ;
        }
    }
    
    return sentences;
}

//function to calculate Coleman-Liau index
int CL_index(string text)
{
    //initialise variables
    int let = letters(text);
    int wor = words(text);
    int sen = sentences(text);
    
    //calculate parameters
    float L = ((float) let / (float) wor) * 100;
    float S = ((float) sen / (float) wor) * 100;
    
    //calculate precise index
    float index = 0.0588 * L - 0.296 * S - 15.8;
    
    //find index rounded to nearest whole number
    int index_round = round(index);
    
    return index_round;
}

//function to print grade based on text
void classify(string text)
{
    //calculate Coleman-Liau index
    int index = CL_index(text);
    
    //classify grade
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}