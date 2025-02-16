#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct Point{
    float x,y;
} Point;

int compare (const void * a, const void * b)
{
    float fa = *(const float*) a;
    float fb = *(const float*) b;
    return (fa > fb) - (fa < fb);
}

float Bundschuh_Zhu_Algorithm(Point *pointset, int n) {
    qsort(pointset, n, sizeof(Point), compare);

    float *x_values = (float *)malloc((n + 2) * sizeof(float));
    float *y_values = (float *)malloc(n * sizeof(float));
    float *y_matrix_values = (float *)malloc(n * sizeof(float));
    
    int y_matrix_size = 0;
    float max_discrepancy = 0.0;

    x_values[0] = 0.0;
    x_values[n + 1] = 1.0;

    for (int i = 0; i < n; i++) {
        x_values[i + 1] = pointset[i].x;
        y_values[i] = pointset[i].y;
    }

    for (int l = 0; l <= n; l++) {
        // Insertion sort
        if (l > 0) {
            int i = y_matrix_size;
            while (i > 0 && y_matrix_values[i - 1] > y_values[l - 1]) {
                y_matrix_values[i] = y_matrix_values[i - 1];
                i--;
            }
            y_matrix_values[i] = y_values[l - 1];
            y_matrix_size++;
        }

        float *matrix_y = (float *)malloc((y_matrix_size + 2) * sizeof(float));
        matrix_y[0] = 0.0;
        for (int i = 0; i < y_matrix_size; i++) {
            matrix_y[i + 1] = y_matrix_values[i];
        }
        matrix_y[y_matrix_size + 1] = 1.0;

        for (int k = 0; k <= l; k++) {
            float point_ratio = (float)k / n;
            float area_one = x_values[l] * matrix_y[k];
            float area_two = x_values[l + 1] * matrix_y[k + 1];
            float discrepancy = fmax(point_ratio - area_one, area_two - point_ratio);
            if (discrepancy > max_discrepancy) {
                max_discrepancy = discrepancy;
            }
        }
        free(matrix_y);
    }

    free(x_values);
    free(y_values);
    free(y_matrix_values);

    return round(max_discrepancy * 1e7) / 1e7;
}

Point *generate_pointset(float x_value, float y_value, char** all_points){
    // 8 is temporary in the line below
    Point *pointset = (float*)malloc(8 * sizeof(float));
}

int remove_duplicates(Point* pointset, int n){
    if (n == 0) return 0;
  
    int j = 0;
    for (int i = 1; i < n - 1; i++) {
        // If a unique element is found, place it at arr[j + 1]
        if (pointset[i].x != pointset[j].x && pointset[i].y != pointset[i].y){
            pointset[++j] = pointset[i];
        }
    }  
      // Return the new ending of array that only contains unique elements
    return j + 1;
}

float *calculate_discrepancies(int num_points){
    float *discrepancies = (float*)malloc(num_points * num_points * sizeof(float));

    char all_points[100][20] = {
        "x,y", "-y,x-y", "-x+y,-x", "-x,-y", "y,-x+y", "x-y,x", 
        "-y,-x", "-x+y,y", "x,x-y", "y,x", "x-y,-y", "-x,-x+y"
    };

    int all_points_length = sizeof(all_points) / sizeof(all_points[0]);

    for(int x = 0; x < num_points + 1; x++){
        for(int y = 0; y < num_points + 1; y++){
            Point* pointset = (Point*)malloc(all_points_length * sizeof(Point));
            pointset = generate_pointset(x, y, all_points);
            // pointset remove duplicates
            int n = sizeof(pointset) / sizeof(pointset[0]);
            discrepancies[x*num_points + y] = Bundschuh_Zhu_Algorithm(pointset, n);
        }
    }
}


int main(){
    char input_symmetry[] = "17f";
    char path[] = "../data/wyckoff_positions_2D_Letters.txt";

    return 0;
}