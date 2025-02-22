#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include "string_manipulation.c"
#include "Bundschuh_Zhu.c"

Point *generate_pointset(float x_value, float y_value, char all_points[][20], int n) {
    Point *pointset = (Point *)malloc(n * sizeof(Point));
    // These mfs here bcs of memory crashes
    if (!pointset) return NULL; 

    char x_str[20], y_str[20];
    // Convert float to string
    sprintf(x_str, "%.1f", fmod(x_value, 1));
    sprintf(y_str, "%.1f", fmod(y_value, 1));
    
    

    for (int i = 0; i < n; i++) {
        char *copy = strdup(all_points[i]);
        if (!copy) continue; // These mfs here bcs of memory crashes

        char *token = strtok(copy, ",");
        if (!token) { free(copy); continue; }

        char *replaced_x = str_replace(token, "x", x_str);
        char *replaced_y = str_replace(replaced_x, "y", y_str);
        float coordinate_x = fmod(evaluate_expression(replaced_x), 1.0);

        free(replaced_x);
        free(replaced_y);

        // These mfs here bcs of memory crashes
        token = strtok(NULL, ",");
        if (!token) { free(copy); continue; }

        replaced_x = str_replace(token, "x", x_str);
        replaced_y = str_replace(replaced_x, "y", y_str);
        float coordinate_y = fmod(evaluate_expression(replaced_y), 1.0);

        //printf("X: %f, Y: %f -> (%f, %f)\n", x_value, y_value, coordinate_x, coordinate_y);

        pointset[i].x = round(coordinate_x * 10.0) / 10.0;
        pointset[i].y = round(coordinate_y * 10.0) / 10.0;

        free(replaced_x);
        free(replaced_y);
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
    // 17f
    char all_points[12][20] = {
        "x,y", "-y,x-y", "-x+y,-x", "-x,-y", "y,-x+y", "x-y,x", 
        "-y,-x", "-x+y,y", "x,x-y", "y,x", "x-y,-y", "-x,-x+y"
    };
    
    int n = sizeof(all_points) / sizeof(all_points[0]);
    int counter = 0;

    for(int x = 0; x < num_points; x++){
        for(int y = 0; y < num_points; y++){
            float x_value = x / (float)num_points;
            float y_value = y / (float)num_points;
            
            Point* pointset = generate_pointset(x_value, y_value, all_points, n);
            
            int unique_n;
            Point* unique_pointset = remove_duplicates(pointset, n, &unique_n);
            
            discrepancies[counter] = Bundschuh_Zhu_Algorithm(unique_pointset, unique_n);
            counter++;

            free(pointset);
            free(unique_pointset);
        }
    }
    return discrepancies;
}

void display_array(float *arr, int size) {
    for(int i = 0; i < size; i++) {
        printf("%f\n", arr[i]);
    }
    printf("\n");
}

int main() {
    int interpolations = 100;
    
    float *discrepancies = calculate_discrepancies(interpolations);
    display_array(discrepancies, interpolations * interpolations);
    free(discrepancies);

    return 0;
}
