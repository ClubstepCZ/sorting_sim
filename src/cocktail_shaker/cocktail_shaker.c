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

void cocktail_shaker_entry_point(int *arr, int n); // Function declaration

void cocktail_shaker_entry_point(int *arr, int n) {
    set_sorting_array(arr);
    int start = 0;
    int end = n - 1;
    int swapped = 1;
    int i;
    int temp;
    WHILE(swapped) {
        swapped = 0;

        FOR(i = start, i < end, i++) {
            IF(arr[i] > arr[i + 1]) {
                SWAP(arr[i], arr[i + 1], temp);
                swapped = 1;
            }
        }
        IF(!swapped) {
            break;
        }
        swapped = 0;
        end--;
        FOR(i = end - 1, i >= start, i--) {
            IF(arr[i] > arr[i + 1]) {
                SWAP(arr[i], arr[i + 1], temp);
                swapped = 1;
            }
        }
        start++;
    }
}
