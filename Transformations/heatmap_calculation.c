#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

typedef struct Point{
    double x,y;
} Point;

//Must free memory after usage, copied from stack overflow
char *str_replace(char *orig, char *rep, char *with) {
    char *result; // the return string
    char *ins;    // the next insert point
    char *tmp;    // varies
    int len_rep;  // length of rep (the string to remove)
    int len_with; // length of with (the string to replace rep with)
    int len_front; // distance between rep and end of last rep
    int count;    // number of replacements

    // sanity checks and initialization
    if (!orig || !rep)
        return NULL;
    len_rep = strlen(rep);
    if (len_rep == 0)
        return NULL; // empty rep causes infinite loop during count
    if (!with)
        with = "";
    len_with = strlen(with);

    // count the number of replacements needed
    ins = orig;
    for (count = 0; (tmp = strstr(ins, rep)); ++count) {
        ins = tmp + len_rep;
    }

    tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);

    if (!result)
        return NULL;

    // first time through the loop, all the variable are set correctly
    // from here on,
    //    tmp points to the end of the result string
    //    ins points to the next occurrence of rep in orig
    //    orig points to the remainder of orig after "end of rep"
    while (count--) {
        ins = strstr(orig, rep);
        len_front = ins - orig;
        tmp = strncpy(tmp, orig, len_front) + len_front;
        tmp = strcpy(tmp, with) + len_with;
        orig += len_front + len_rep; // move to next "end of rep"
    }
    strcpy(tmp, orig);
    return result;
}

double evaluate_expression(char *string) {
    double result = 0.0;
    double num = 0.0;
    char op = '+';  // Default to addition
    int i = 0;

    while (string[i]) {
        // Skip whitespace
        if (isspace(string[i])) {
            i++;
            continue;
        }

        // Parse a number
        if (isdigit(string[i]) || string[i] == '.') {
            num = strtod(&string[i], NULL);

            // Move i forward past the number
            while (isdigit(string[i]) || string[i] == '.') i++;

            // Apply the previous operator
            if (op == '+') {
                result += num;
            } else if (op == '-') {
                result -= num;
            }
        } 
        
        // Read the operator
        if (string[i] == '+' || string[i] == '-') {
            op = string[i];
            i++;
        }
    }

    return result;
}

int compare (const void * a, const void * b) {
    double fa = ((Point*)a)->x;
    double fb = ((Point*)b)->x;
    return (fa > fb) - (fa < fb);
}

double Bundschuh_Zhu_Algorithm(Point *pointset, int n) {
    qsort(pointset, n, sizeof(Point), compare);

    double *x_values = (double *)malloc((n + 2) * sizeof(double));
    double *y_values = (double *)malloc(n * sizeof(double));
    double *y_matrix_values = (double *)malloc(n * sizeof(double));
    
    int y_matrix_size = 0;
    double max_discrepancy = 0.0;

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

        double *matrix_y = (double *)malloc((y_matrix_size + 2) * sizeof(double));
        matrix_y[0] = 0.0;
        for (int i = 0; i < y_matrix_size; i++) {
            matrix_y[i + 1] = y_matrix_values[i];
        }
        matrix_y[y_matrix_size + 1] = 1.0;

        for (int k = 0; k <= l; k++) {
            double point_ratio = (double)k / n;
            double area_one = x_values[l] * matrix_y[k];
            double area_two = x_values[l + 1] * matrix_y[k + 1];
            double discrepancy = fmax(point_ratio - area_one, area_two - point_ratio);
            if (discrepancy > max_discrepancy) {
                max_discrepancy = discrepancy;
            }
        }
        free(matrix_y);
    }

    free(x_values);
    free(y_values);
    free(y_matrix_values);

    return max_discrepancy;
}

double modulo_positive(double a, double b) {
    if (fabs(b) < 1e-10) return 0.0;  // Prevent division by zero
    double result = fmod(a, b);
    if (result < 0) result += b;  // Ensures result is always non-negative
    return result;
}

Point *generate_pointset(double x_value, double y_value, char **all_points, int n) {
    if (!all_points || n <= 0) return NULL;  // Handle invalid input
    // Throwaway variable
    double int_part;
    Point *pointset = (Point*)calloc(n, sizeof(Point));
    if (!pointset) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    char x_string[50];
    char y_string[50];
    snprintf(x_string, sizeof(x_string), "%f", x_value);
    snprintf(y_string, sizeof(y_string), "%f", y_value);

    for (int i = 0; i < n; i++) {
        if (!all_points[i]) continue; // Handle null strings

        char *temp1 = str_replace(all_points[i], "x", x_string);
        if (!temp1) continue;  // Skip this iteration if memory allocation fails
        
        char *temp2 = str_replace(temp1, "y", y_string);
        free(temp1);  // Free old allocation
        if (!temp2) continue;  
        
        char *copy = strdup(temp2);
        free(temp2);  
        if (!copy) continue;

        // Extract x and y values, NEEDS MODULO here
        char *token = strtok(copy, ",");
        if (token) pointset[i].x = modulo_positive(evaluate_expression(token), 1.0);

        token = strtok(NULL, ",");
        if (token) pointset[i].y = modulo_positive(evaluate_expression(token), 1.0);

        free(copy);

    }

    return pointset;
}

void display_pointset(Point *pointset, int n){
    for(int i = 0; i < n; i++){
        printf("%f, %f\n", pointset[i].x, pointset[i].y);
    }
}

double *discrepancy_calculation(char** all_points, int n, int resolution){
    double *discrepancies = (double*)calloc((resolution + 1) * (resolution + 1), sizeof(double));
    int position = 0;
    for(int x = 0; x < resolution; x++){
        for(int y = 0; y < resolution; y++){
            Point *pointset = generate_pointset(x / (double)resolution, y / (double)resolution, all_points, n);
            double discrepancy = Bundschuh_Zhu_Algorithm(pointset, n);
            discrepancies[position] = discrepancy;
            position++;

            if (pointset) free(pointset);
        }
    }
    return discrepancies;
}

void free_discrepancies(double *discrepancies) {
    free(discrepancies);
}

int main(){
    char *all_points[] = {
        "x,y", "-y,x-y", "-x+y,-x", "-x,-y", "y,-x+y", "x-y,x", 
        "-y,-x", "-x+y,y", "x,x-y", "y,x", "x-y,-y", "-x,-x+y"
    };
    int n = 12;
    double *discrepancies = discrepancy_calculation(all_points, n, 100);
    free_discrepancies(discrepancies);
    
    return 0;
}