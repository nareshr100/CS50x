#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //iterate through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //calculate average of RGB
            int avg = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            avg = round(avg / 3.0);

            //set RGB values to average
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tempimage[height][width];

    //iterate through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //store pixel RGB values in temp image arra
            tempimage[i][j].rgbtBlue = image[i][j].rgbtBlue;
            tempimage[i][j].rgbtGreen = image[i][j].rgbtGreen;
            tempimage[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }

    //flip image about y-axis
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][width - j - 1].rgbtBlue = tempimage[i][j].rgbtBlue;
            image[i][width - j - 1].rgbtGreen = tempimage[i][j].rgbtGreen;
            image[i][width - j - 1].rgbtRed = tempimage[i][j].rgbtRed;
        }
    }

    return;
}

void blur_pixel(int i, int j, int start_k, int end_k, int start_l, int end_l, int height, int width, RGBTRIPLE image[height][width], 
                RGBTRIPLE image2[height][width])
{
    float avgBlue = 0.0;
    float avgGreen = 0.0;
    float avgRed = 0.0;

    //find average of all neighbours
    for (int k = start_k; k < end_k + 1; k++)
    {
        int index1 = i + k;

        for (int l = start_l; l < end_l + 1; l++)
        {
            int index2 = j + l;

            avgBlue += image2[index1][index2].rgbtBlue;
            avgGreen += image2[index1][index2].rgbtGreen;
            avgRed += image2[index1][index2].rgbtRed;
        }
    }

    float n = (end_k - start_k + 1.0) * (end_l - start_l + 1.0);
    //printf("%f ", n);

    avgBlue = round(avgBlue / n);
    avgGreen = round(avgGreen / n);
    avgRed = round(avgRed / n);

    image[i][j].rgbtBlue = avgBlue;
    image[i][j].rgbtGreen = avgGreen;
    image[i][j].rgbtRed = avgRed;

    return;
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //create temporary image
    RGBTRIPLE image2[height][width];

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

//function to implement edge
void edge_pixel(int i, int j, int height, int width, RGBTRIPLE image[height][width], RGBTRIPLE image2[height + 2][width + 2], 
                int Kx[3][3], int Ky[3][3])
{
    int GxBlue = 0;
    int GxGreen = 0;
    int GxRed = 0;

    int GyBlue = 0;
    int GyGreen = 0;
    int GyRed = 0;

    //find average of all neighbours
    for (int k = 0; k < 3; k++)
    {
        int index1 = i + k;

        for (int l = 0; l < 3; l++)
        {
            int index2 = j + l;

            GxBlue += (image2[index1][index2].rgbtBlue * Kx[k][l]);
            GxGreen += (image2[index1][index2].rgbtGreen * Kx[k][l]);
            GxRed += (image2[index1][index2].rgbtRed * Kx[k][l]);

            GyBlue += (image2[index1][index2].rgbtBlue * Ky[k][l]);
            GyGreen += (image2[index1][index2].rgbtGreen * Ky[k][l]);
            GyRed += (image2[index1][index2].rgbtRed * Ky[k][l]);
        }
    }

    int GBlue = round(sqrt(pow(GxBlue, 2) + pow(GyBlue, 2)));
    int GGreen = round(sqrt(pow(GxGreen, 2) + pow(GyGreen, 2)));
    int GRed = round(sqrt(pow(GxRed, 2) + pow(GyRed, 2)));

    if (GBlue > 255)
    {
        GBlue = 255;
    }
    if (GGreen > 255)
    {
        GGreen = 255;
    }
    if (GRed > 255)
    {
        GRed = 255;
    }

    image[i][j].rgbtBlue = GBlue;
    image[i][j].rgbtGreen = GGreen;
    image[i][j].rgbtRed = GRed;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //Create kernel for Gx and Gy
    int Kx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Ky[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    //create temp array
    RGBTRIPLE image2[height + 2][width + 2];

    //copy to new array
    for (int i = 0; i < height + 2; i++)
    {
        for (int j = 0; j < width + 2; j++)
        {
            if (i == 0 || i == height + 1 || j == 0 || j == width + 1)
            {
                image2[i][j].rgbtBlue = 0;
                image2[i][j].rgbtGreen = 0;
                image2[i][j].rgbtRed = 0;
            }
            else
            {
                image2[i][j] = image[i - 1][j - 1];
            }
        }
    }

    //iterate through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            edge_pixel(i, j, height, width, image, image2, Kx, Ky);
        }
    }

    return;
}