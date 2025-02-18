#include <stdio.h>
#include <stdlib.h>
#define _USE_MATH_DEFINES
#include <math.h>
#include <complex.h>

// For 3D cases
// Complex numbers won't be confirmed by interpreter

typedef struct Point{
    double x,y,z;
} Point;

double halton_sequence(int index, int base){
    double f = 1.0;
    double r = 0.0;
    while(index > 0){
        f = f/base;
        r = r + f * fmod(index, base);
        index = floor(index/base);
    }
    return r;
}

Point* halton_sequence_pointset(int n){
    Point *pointset = (Point*)malloc(n * sizeof(Point));
    for(int i = 0; i < n; i++){
        pointset[i].x = halton_sequence(i, 2);
        pointset[i].y = halton_sequence(i, 3);
        pointset[i].z = halton_sequence(i, 4);
    }
    return pointset;
}

double dot_product(double x_vector[], int h_vector[], int d){
    double result = 0.0;
    for (int i = 0; i < d; i++)
        result += x_vector[i]*(double)h_vector[i];
    return result;
}

// C compiler can't have float _Complex

double _Complex e_function(double x_vector[], int h_vector[], int dimension){
    return cexp(I * 2 * M_PI * dot_product(x_vector, h_vector, dimension));
}

double _Complex Sn_function(Point* pointset, int *h_vector, int dimension, int n){
    double _Complex sigma = 0.0 + 0.0 * I;

    for(int i = 0; i < n; i++){
        double x_vector[3] = {pointset[i].x, pointset[i].y, pointset[i].z};
        sigma += e_function(x_vector, h_vector, dimension);
    }

    return (1.0 / n) * sigma;
}

double  r(int *h_vector, int dimension){
    double return_value = 1.0;
    for(int j = 0; j < dimension; j++){
        return_value *= fmax(1, abs(h_vector[j]));
    }
    return return_value;
}

double Diaphony_Function(Point* pointset, int upper_boundary, int lower_boundary, int dimension, int n){
    double diaphony_value = 0.0;
    int iterations = upper_boundary + abs(lower_boundary) + 1;
    
    for(int h = lower_boundary; h <= upper_boundary; h++){
        for(int k = lower_boundary; k <= upper_boundary; k++){
            for(int l = lower_boundary; l <= upper_boundary; l++){
                int h_vector[3] = {h, k, l};
                diaphony_value += pow(r(h_vector, dimension), -2.0) * pow(cabs(Sn_function(pointset, h_vector, dimension, n)), 2.0);
            }
        } 
    }

    return sqrt(diaphony_value);
}

void display_pointset(Point *pointset, int n){
    for(int i = 0; i < n; i++){
        printf("(%f,%f,%f)\n", pointset[i].x, pointset[i].y, pointset[i].z);
    }
}

void check_C_version(){
    if (__STDC_VERSION__ >= 201710L)
        printf("We are using C17!\n");
    else if (__STDC_VERSION__ >= 201112L)
        printf("We are using C11!\n");
    else if (__STDC_VERSION__ >= 199901L)
        printf("We are using C99!\n");
    else
        printf("We are using C89/C90!\n");
}

int main() {
    int n = 10; // Number of points
    int d = 3; // Dimensions 
    
    // Parameters for diaphony
    int lower_boundary = -10;
    int upper_boundary = 10;
    
    Point *pointset = halton_sequence_pointset(n);
    int iterations = upper_boundary + abs(lower_boundary);
    double diaphony_value = Diaphony_Function(pointset, upper_boundary, lower_boundary, d, n);

    printf("%f", diaphony_value);
    free(pointset);

    return 0;
}

