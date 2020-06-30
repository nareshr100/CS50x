#include <math.h>
#include <stdio.h>

void blur(int height, int width, int image[height][width]);

int main(void)
{
    int image[3][3] = {{10, 40, 70}, {110, 120, 130}, {200, 220, 240}};

    blur(3, 3, image);
}

void blur_pixel(int i, int j, int start_k, int end_k, int start_l, int end_l, int height, int width, int image[height][width], int image2[height][width])
{
    printf("pixel [%i][%i]\n", i, j);

    float avg = 0.0;

    printf("initial avg = %f\n", avg);

    //find average of all neighbours
    for (int k = start_k; k < end_k + 1; k++)
    {
        int index1 = i + k;

        for (int l = start_l; l < end_l + 1; l++)
        {
            int index2 = j + l;

            avg += image2[index1][index2];

            printf("index1 = %i, index2 = %i, avg = %f\n", index1, index2, avg);
        }
    }

    float n = (end_k - start_k + 1.0) * (end_l - start_l + 1.0);
    //printf("%f ", n);

    avg = round(avg / n);

    printf("final avg of [%i][%i] = %f\n", i, j, avg);

    image[i][j] = avg;



    return;
}


// Blur image
void blur(int height, int width, int image[height][width])
{
    //create temporary image
    int image2[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            image2[i][j] = image[i][j];
        }
    }

    //iterate through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            //check if top left corner
            if (i == 0 && j == 0)
            {
                blur_pixel(i, j, 0, 1, 0, 1, height, width, image, image2);
            }
            //check if top right corner
            else if ((i == 0) && (j == width - 1))
            {
                blur_pixel(i, j, 0, 1, -1, 0, height, width, image, image2);
            }
            //check if bottom right corner
            else if ((i == height - 1) && (j == width - 1))
            {
                blur_pixel(i, j, -1, 0, -1, 0, height, width, image, image2);
            }
            //check if bottom left corner
            else if ((i == height - 1) && (j == 0))
            {
                blur_pixel(i, j, -1, 0, 0, 1, height, width, image, image2);
            }
            //check if left edge
            else if ((j == 0) && (i != 0) && (i != height - 1))
            {
                blur_pixel(i, j, -1, 1, 0, 1, height, width, image, image2);
            }
            //check if right edge
            else if ((j == width - 1) && (i != 0) && (i != height - 1))
            {
                blur_pixel(i, j, -1, 1, -1, 0, height, width, image, image2);
            }
            //check if top edge
            else if ((i == 0) && (j != 0) && (j != width - 1))
            {
                blur_pixel(i, j, 0, 1, -1, 1, height, width, image, image2);
            }
            //check if bottom edge
            else if ((i == height - 1) && (j != 0) && (j != width - 1))
            {
                blur_pixel(i, j, -1, 0, -1, 1, height, width, image, image2);
            }
            // else middle pixel
            else
            {
                blur_pixel(i, j, -1, 1, -1, 1, height, width, image, image2);
            }
        }
    }

    return;
}