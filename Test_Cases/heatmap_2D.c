#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct Point{
    float x, y;
} Point;

int compare (const void * a, const void * b) {
    float fa = ((Point*)a)->x;
    float fb = ((Point*)b)->x;
    return (fa > fb) - (fa < fb);
}

Point *test_pointset(){
    Point *pointset = (Point*)malloc(32*sizeof(Point));
    for(int k = 0; k < 33; k++){
        pointset[k].x = k / 32.0;
        pointset[k].y = fmod(7.0 * k / 32.0, 1);
    }
    return pointset;
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

float evaluate_expression(const char *expr, float x, float y) {
    char buffer[20];
    snprintf(buffer, sizeof(buffer), expr, x, y);
    return fmod(atof(buffer), 1.0);
}

Point *generate_pointset(float x_value, float y_value, char all_points[][20], int n) {
    Point *pointset = (Point *)malloc(n * sizeof(Point));

    for (int i = 0; i < n; i++) {
        char *copy = strdup(all_points[i]);
        char *token = strtok(copy, ",");
        
        float coordinate_x = evaluate_expression(token, x_value, y_value);
        token = strtok(NULL, ",");
        float coordinate_y = evaluate_expression(token, x_value, y_value);

        pointset[i].x = round(coordinate_x * 10) / 10.0;
        pointset[i].y = round(coordinate_y * 10) / 10.0;

        free(copy);
    }

    return pointset;
}

int point_compare(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    if (p1->x != p2->x) return (p1->x > p2->x) - (p1->x < p2->x);
    return (p1->y > p2->y) - (p1->y < p2->y);
}

Point* remove_duplicates(Point* pointset, int n, int *unique_n){
    if (n == 0) return NULL;
    int j = 0;

    for (int i = 1; i < n; i++) {
        if (pointset[i].x != pointset[j].x || pointset[i].y != pointset[j].y){
            pointset[++j] = pointset[i];
        }
    }

    *unique_n = j + 1;  // Store unique count

    Point *set_pointset = (Point*)malloc((*unique_n) * sizeof(Point));
    memcpy(set_pointset, pointset, (*unique_n) * sizeof(Point));
    return set_pointset;
}

float *calculate_discrepancies(int num_points){
    float *discrepancies = (float*)calloc(num_points * num_points, sizeof(float));

    char all_points[12][20] = {
        "x,y", "-y,x-y", "-x+y,-x", "-x,-y", "y,-x+y", "x-y,x", 
        "-y,-x", "-x+y,y", "x,x-y", "y,x", "x-y,-y", "-x,-x+y"
    };
    
    int n = sizeof(all_points) / sizeof(all_points[0]);

    for(int x = 0; x < num_points; x++){
        for(int y = 0; y < num_points; y++){
            float x_value = (float)x / num_points;
            float y_value = (float)y / num_points;
            
            Point* pointset = generate_pointset(x_value, y_value, all_points, n);
            if (pointset == NULL) continue;
            
            int unique_n;
            Point* unique_pointset = remove_duplicates(pointset, n, &unique_n);
            
            discrepancies[x * num_points + y] = Bundschuh_Zhu_Algorithm(unique_pointset, unique_n);
            
            free(pointset);
            free(unique_pointset);
        }
    }
    return discrepancies;
}

void display_array(float *arr, int size) {
    for(int i = 0; i < size; i++) {
        printf("%f ", arr[i]);
    }
    printf("\n");
}

int main() {
    int interpolations = 5;

    float *discrepancies = calculate_discrepancies(interpolations);
    display_array(discrepancies, interpolations * interpolations);
    free(discrepancies);
    
    return 0;
}
