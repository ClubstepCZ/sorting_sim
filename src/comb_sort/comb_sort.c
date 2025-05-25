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

// source: https://cs.wikipedia.org/wiki/Comb_sort

void comb_sort_entry_point(int *arr, int n); // Function declaration

void comb_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);

    const float shrink = 1.3f;
    int gap = n;
    int swap;
    int swapped = 0;

    WHILE(gap > 1 || swapped) {
        IF(gap > 1) {
            gap = (int)((float)gap / shrink);
            IF(gap < 1) {
                gap = 1;
            }
        }

        swapped = 0;

        FOR(int i = 0, i + gap < n, i++) {
            IF(arr[i] > arr[i + gap]) {
                SWAP(arr[i], arr[i + gap], swap);
                swapped = 1;
            }
        }
    }
}
