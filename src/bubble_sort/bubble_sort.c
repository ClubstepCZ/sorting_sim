#include <stdio.h>
#include "../elementary_ops.h"
#include "../memory_tracker.h"

void bubble_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);
    int i, j;
    int temp;
    FOR(i = 0, i < n - 1, i++) {
        FOR(j = 0, j < n - i - 1, j++) {
            IF(arr[j] > arr[j + 1]) {
                SWAP(arr[j], arr[j + 1], temp);
            }
        }
    }
}
