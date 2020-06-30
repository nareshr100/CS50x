#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

string lowercase(string key);
bool test_alphabetic(string key);
bool test_unique(string key);
void make_cipher(string key);

int main(int argc, string argv[])
{
    int error = 0;
    string key = argv[1];

    //if no key entered set error to 1
    if (argc == 2 && strlen(key) == 26 && test_alphabetic(key) == true && test_unique(key) == true)
    {
        //make cypher text using lowercase version of key
        make_cipher(lowercase(key));
    }
    else
    {
        //set error to 1
        printf("Inputted key is invalid. Please choose a key");
        printf(" with 26 unique alphabetic characters\n");
        error = 1;
    }

    return error;
}

//function to find whether every character in a string is alphabetic
bool test_alphabetic(string key)
{
    bool alpha = true;

    for (int i = 0; i < strlen(key); i++)
    {
        int c = (int) key[i];

        if (c < 65 || (c > 90 && c < 97) || c > 122)
        {
            //set alpha to false and break loop
            //implies non-alphabetic character found
            alpha = false;
            break;
        }
        else
        {
            //do nothing
            ;
        }
    }

    return alpha;
}

//function to find whether every character in a string is unique
bool test_unique(string key)
{
    bool u = true;

    for (int i = 0; i < strlen(key); i++)
    {
        int c = (int) key[i];

        if (u == true)
        {
            for (int j = 0; j < strlen(key); j++)
            {
                if (j == i)
                {
                    //skip if testing against self
                    ;
                }
                else if (c == (int) key[j])
                {
                    //set alpha to false and break loop
                    //implies non-unique character found
                    u = false;
                    break;
                }
                else
                {
                    //do nothing
                    ;
                }
            }
        }
        else
        {
            //if non-unique character found exit loop and return false
            break;
        }

    }

    return u;
}

//function to convert all uppercase to lower case for key as my convention
string lowercase(string key)
{
    for (int i = 0; i < strlen(key); i++)
    {
        //find integer value of char (ASCII)
        int c = (int) key[i];

        //check if uppercase
        if (c > 64 && c < 91)
        {
            //if uppercase make lowercase
            c += 32;
            key[i] = (char) c;
        }
        else
        {
            //if not do nothing
            ;
        }
    }

    return key;
}

//function to turn text into cypher text
string cipher(string key, string text)
{
    //iterate through text
    for (int i = 0; i < strlen(text); i++)
    {
        //find text character
        int c = (int) text[i];

        //check if tect character is originally uppercase
        if (c > 64 && c < 91)
        {

            //find poistion of text character in alphabet
            int n = c - 64;

            //find key character at that position
            int k = (int) key[n - 1];

            //if uppercase keep uppercase with key
            text[i] = (char)(k - 32);
        }
        else if (c > 96 && c < 123)
        {
            //find poistion of text character in alphabet
            int n = c - 96;

            //find key character at that position
            int k = (int) key[n - 1];

            //if uppercase keep uppercase with key
            text[i] = (char) k;
        }
        else
        {
            //do nothing
            ;
        }
    }

    return text;
}

//function to get text from user and return cyphertext

void make_cipher(string key)
{
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: %s\n", cipher(key, plaintext));
}