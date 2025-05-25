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

void cycle_sort_entry_point(int *arr, int n); // Function declaration

void cycle_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);

    int writes = 0;
    int temp;

    FOR(int cycle_start = 0, cycle_start < n - 1, cycle_start++) {
        int item = arr[cycle_start];
        int pos = cycle_start;

        FOR(int i = cycle_start + 1, i < n, i++) {
            IF(arr[i] < item) {
                pos++;
            }
        }

        IF(pos == cycle_start) {
            continue;
        }

        WHILE(item == arr[pos]) {
            pos++;
        }

        IF(pos != cycle_start) {
            temp = arr[pos];
            arr[pos] = item;
            item = temp;
            TRACK_CHANGE(pos);
            writes++;
        }

        WHILE(pos != cycle_start) {
            pos = cycle_start;

            FOR(int i = cycle_start + 1, i < n, i++) {
                IF(arr[i] < item) {
                    pos++;
                }
            }

            WHILE(item == arr[pos]) {
                pos++;
            }

            temp = arr[pos];
            arr[pos] = item;
            item = temp;
            TRACK_CHANGE(pos);
            writes++;
        }
    }
}
