#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "../memory_tracker.h"
#include "../elementary_ops.h"

/*
 * Use the following macros instead of standard C constructs:
 *
 *  - FOR(init, cond, update)       instead of: for (init; cond; update)
 *  - IF(condition)                 instead of: if (condition)
 *  - WHILE(condition)              instead of: while (condition)
 *  - SWAP(a, b, temp)              instead of: swapping two variables
 *  - TRACK_CHANGE(index)           to track manual changes in array
 *  - ADD(a, b), SUBTRACT(a, b), MULTIPLY(a, b), DIVIDE(a, b)
 *                                  instead of: a + b, a - b, a * b, a / b
 *
 * For recursion, use:
 *  - CALL_FUNCTION_VOID(fn, ...)   instead of: fn(...)
 *  - CALL_FUNCTION_RETURN(fn, ...) instead of: return fn(...)
 *
 * These macros ensure correct counting of elementary operations,
 * memory usage, and enable proper visualization.
 */

// source: https://en.wikipedia.org/wiki/Pancake_sorting

void pancake_sort_entry_point(int *arr, int n); // Function declaration

void flip(int *arr, int i) {
    int start = 0;
    int temp;
    WHILE(start < i) {
        SWAP(arr[start], arr[i], temp);
        start++;
        i--;
    }
}

int find_max_index(int *arr, int n) {
    int max_idx = 0;
    FOR(int i = 1, i < n, i++) {
        IF(arr[i] > arr[max_idx]) {
            max_idx = i;
        }
    }
    return max_idx;
}

void pancake_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);

    FOR(int curr_size = n, curr_size > 1, curr_size--) {
        int max_idx = CALL_FUNCTION_RETURN(find_max_index, arr, curr_size);

        IF(max_idx != curr_size - 1) {
            IF(max_idx > 0) {
                CALL_FUNCTION_VOID(flip, arr, max_idx);
            }
            CALL_FUNCTION_VOID(flip, arr, curr_size - 1);
        }
    }
}
