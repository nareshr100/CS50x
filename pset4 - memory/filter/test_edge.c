#include <math.h>
#include <stdio.h>

void edges(int height, int width, int image[height][width]);

int main(void)
{
    int image[3][3] = {{0, 0, 40}, {20, 30, 80}, {20, 30, 50}};

    edges(3, 3, image);
}

//function to implement edge
void edge_pixel(int i, int j, int height, int width, int image[height][width], int image2[height + 2][width + 2], int Kx[3][3], int Ky[3][3])
{

    int Gx = 0;
    int Gy = 0;

    //find average of all neighbours
    for (int k = 0; k <= 2; k++)
    {
        int index1 = i+k;

        for (int l = 0; l <= 2; l++)
        {
            int index2 = j+l;

            Gx += (image2[index1][index2] * Kx[k][l]);
            Gy += (image2[index1][index2] * Ky[k][l]);
            printf("i = %i, j = %i, image[%i][%i] = %i, Kx[%i][%i] = %i, Ky[%i][%i] = %i, Gx = %i, Gy = %i\n", i, j, index1, index2, image2[index1][index2], k, l, Kx[k][l], k, l, Ky[k][l], Gx, Gy);
        }
    }

    int G = round(sqrt(pow(Gx, 2) + pow(Gy, 2)));

    if(G > 255)
    {
        G = 255;
    }

    image[i][j] = G;
    printf("G = %i\n", G);
}

// Detect edges
void edges(int height, int width, int image[height][width])
{
    //Create kernel for Gx and Gy
    int Kx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Ky[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};


    //create temp array with one pixel black border
    int image2[height+2][width+2];

    //copy to new array with black border
    for (int i = 0; i < height + 2; i++)
    {
        for (int j = 0; j < width + 2; j++)
        {
            if (i == 0 || i == height + 1 || j == 0 || j == width + 1)
            {
                image2[i][j] = 0;
            }
            else
            {
                image2[i][j] = image[i-1][j-1];

            }
            printf("image[%i][%i] = %i\n", i, j, image2[i][j]);
        }
    }

    //iterate through all pixels of original image leaving single pixel border
    for (int i = 0; i < height ; i++)
    {
        for (int j = 0; j < width; j++)
        {
            edge_pixel(i, j, height, width, image, image2, Kx, Ky);
        }
    }

    return;
}