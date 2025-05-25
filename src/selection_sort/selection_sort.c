#include <stddef.h>
#include "../elementary_ops.h"
#include "../memory_tracker.h"

void selection_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);
    FOR(int i = 0, i < n - 1, i++) {
        int min_idx = i;
        FOR(int j = i + 1, j < n, j++) {
            IF(arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        int temp;
        SWAP(arr[i], arr[min_idx], temp);
    }
}

