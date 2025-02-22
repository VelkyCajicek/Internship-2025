#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

// Structure to hold point coordinates
typedef struct {
    float x, y;
} Point;

// Function to replace substrings in a string
char *str_replace(char *orig, const char *rep, const char *with) {
    char *result, *ins, *tmp;
    int len_rep, len_with, len_front, count;

    if (!orig || !rep || (len_rep = strlen(rep)) == 0) return NULL;
    len_with = strlen(with);
    
    for (ins = orig, count = 0; (tmp = strstr(ins, rep)); ++count) ins = tmp + len_rep;
    
    tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);
    if (!result) return NULL;
    
    while (count--) {
        ins = strstr(orig, rep);
        len_front = ins - orig;
        tmp = strncpy(tmp, orig, len_front) + len_front;
        tmp = strcpy(tmp, with) + len_with;
        orig += len_front + len_rep;
    }
    strcpy(tmp, orig);
    return result;
}

// Function to evaluate simple expressions (assumes input is well-formed)
float evaluate_expression(char *expr) {
    float result = 0.0;
    float num = 0.0;
    char op = '+';

    while (*expr) {
        if (isdigit(*expr) || *expr == '.') {
            num = strtof(expr, &expr);
        }
        if (*expr == '+' || *expr == '-' || *expr == '\0') {
            if (op == '+') result += num;
            else if (op == '-') result -= num;
            op = *expr;
        }
        if (*expr) expr++;
    }
    return fmod(result, 1.0);
}

// Function to generate pointset based on given formulas
Point *generate_pointset(float x, float y, char all_points[][20], int n) {
    Point *pointset = (Point *)malloc(n * sizeof(Point));
    if (!pointset) return NULL;

    char x_str[10], y_str[10];
    sprintf(x_str, "%.2f", x);
    sprintf(y_str, "%.2f", y);

    for (int i = 0; i < n; i++) {
        char *expr_x = str_replace(all_points[i], "x", x_str);
        char *expr_y = str_replace(expr_x, "y", y_str);

        pointset[i].x = round(evaluate_expression(expr_y) * 10.0) / 10.0;
        pointset[i].y = round(evaluate_expression(expr_y) * 10.0) / 10.0;

        free(expr_x);
        free(expr_y);
    }
    return pointset;
}

// Function to remove duplicate points
Point *remove_duplicates(Point *pointset, int n, int *unique_n) {
    if (n == 0) return NULL;
    int j = 0;
    for (int i = 1; i < n; i++) {
        if (pointset[i].x != pointset[j].x || pointset[i].y != pointset[j].y) {
            pointset[++j] = pointset[i];
        }
    }
    *unique_n = j + 1;
    Point *unique_points = (Point *)malloc((*unique_n) * sizeof(Point));
    memcpy(unique_points, pointset, (*unique_n) * sizeof(Point));
    return unique_points;
}

// Placeholder for discrepancy algorithm (to be implemented)
float Bundschuh_Zhu_Algorithm(Point *pointset, int n) {
    return 0.5; // Dummy value for testing
}

// Function to calculate discrepancies
float *calculate_discrepancies(int interpolations) {
    float *discrepancies = (float *)calloc(interpolations * interpolations, sizeof(float));
    char all_points[12][20] = {"x,y", "-y,x-y", "-x+y,-x", "-x,-y", "y,-x+y", "x-y,x",
                               "-y,-x", "-x+y,y", "x,x-y", "y,x", "x-y,-y", "-x,-x+y"};
    int n = 12;

    for (int x = 0; x < interpolations; x++) {
        for (int y = 0; y < interpolations; y++) {
            float x_val = (float)x / interpolations;
            float y_val = (float)y / interpolations;
            Point *pointset = generate_pointset(x_val, y_val, all_points, n);
            int unique_n;
            Point *unique_points = remove_duplicates(pointset, n, &unique_n);
            discrepancies[x * interpolations + y] = Bundschuh_Zhu_Algorithm(unique_points, unique_n);
            free(pointset);
            free(unique_points);
        }
    }
    return discrepancies;
}

void display_array(float *arr, int size) {
    for (int i = 0; i < size; i++) {
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