#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include<cs50.h>

typedef uint8_t BYTE;

typedef struct block
{
    BYTE buffer[512];
}
block;

bool test_JPEG(BYTE *buffer);
//void make_JPEG(void *ptr, int i);

int main(int argc, char *argv[])
{
    //check that exactly one command line argument entered
    if (argc != 2)
    {
        printf("Usage: recover name\n");
        return 1;
    }

    //attempt to open file
    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        //if fails to open inform user
        perror("File failed to open");
        return 1;
    }

    /*//find length of file
    fseek(file, 0, SEEK_END); // seek to end of file
    long len = ftell(file); // get current file pointer
    fseek(file, 0, SEEK_SET); // seek back to beginning of file*/

    //find number of blocks in file
    //int n = len / sizeof(block);

    //initilaise JPEG counter
    int counter = 0;

    //create bufferarray to store JPEG
    BYTE buffer[512];

    //create file to write JPEG in, initialised to NULL
    FILE *img = NULL;

    //keep running until block is empty/end of file
    while (fread(buffer, 512, 1, file) == 1)
    {
        if (test_JPEG(buffer))
        {
            //if start of buffer indicates buffer

            if (counter == 0)
            {
                //if first image make new wile for writing
                //create string to name file
                char filename[8];
                sprintf(filename, "%03i.jpg", counter);

                //open file with correct filename
                img = fopen(filename, "w");

                //write to JPEG file
                fwrite(buffer, sizeof(BYTE), 512, img);

                //increment counter
                counter++;
            }
            else
            {
                //close previous file
                fclose(img);

                //create string to name file
                char filename[8];
                sprintf(filename, "%03i.jpg", counter);

                //open file with correct filename
                img = fopen(filename, "w");

                //write to JPEG file
                fwrite(buffer, sizeof(BYTE), 512, img);

                //increment counter
                counter++;
            }
        }
        else if (counter > 0)
        {
            //write to JPEG file
            fwrite(buffer, sizeof(BYTE), 512, img);
        }
    }
}

//function to test if block has start of a JPEG
bool test_JPEG(BYTE *buffer)
{
    //check for starting signature 0xff 0xd8 0xff and then > 192
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return true;
    }

    return false;
}

/*//function to make file for jpeg and name i from location
void make_JPEG(void *ptr, int i)
{
    //create string to name file
    char filename[8];
    sprintf(filename, "%03i.jpg", i);

    //open file with correct filename
    FILE *img = fopen(filename, "w");

    //write to JPEG file
    fwrite(ptr, sizeof(BYTE), 512, img);

}*/