#include <ctype.h>

// Must free memory after usage, copied from stack overflow
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

#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

float evaluate_expression(const char *string) {
    float result = 0.0, current_number = 0.0;
    char operator = '+'; // Default operator
    int decimal_place = 0;

    while (*string) {
        if (isdigit(*string)) {
            if (decimal_place) {
                current_number += (*string - '0') / (10.0 * decimal_place);
                decimal_place *= 10;
            } else {
                current_number = current_number * 10 + (*string - '0');
            }
        } else if (*string == '.') {
            decimal_place = 1; // Start tracking decimal places
        } else if (*string == '+' || *string == '-' || *string == '*' || *string == '/') {
            // Compute previous value before updating operator
            if (operator == '+') result += current_number;
            else if (operator == '-') result -= current_number;
            else if (operator == '*') result *= current_number;
            else if (operator == '/') result /= current_number;

            current_number = 0;
            decimal_place = 0;
            operator = *string;
        }
        string++;
    }

    // Final computation
    if (operator == '+') result += current_number;
    else if (operator == '-') result -= current_number;
    else if (operator == '*') result *= current_number;
    else if (operator == '/') result /= current_number;

    return result;
}

