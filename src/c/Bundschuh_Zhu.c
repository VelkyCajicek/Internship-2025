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