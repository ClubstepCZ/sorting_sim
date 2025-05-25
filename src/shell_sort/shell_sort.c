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

void shell_sort_entry_point(int *arr, int n); // Function declaration

void shell_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);
    int gap, i, j, temp;

    FOR(gap = DIVIDE(n, 2), gap > 0, gap = DIVIDE(gap, 2)) {
        FOR(i = gap, i < n, ++i) {
            temp = arr[i];
            j = i;

            WHILE(j >= gap && arr[j - gap] > temp) {
                arr[j] = arr[j - gap];
                TRACK_CHANGE(j);
                j = SUBTRACT(j, gap);
            }

            arr[j] = temp;
            TRACK_CHANGE(j);
        }
    }
}
