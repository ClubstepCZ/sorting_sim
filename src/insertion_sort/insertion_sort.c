#include <stddef.h>
#include "../elementary_ops.h"
#include "../memory_tracker.h"

void insertion_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);
    FOR(int i = 1, i < n, i++) {
        int key = arr[i];
        int j = i - 1;
        WHILE(j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            TRACK_CHANGE(j + 1);
            j = SUBTRACT(j, 1);
        }
        arr[j + 1] = key;
        TRACK_CHANGE(j + 1);
    }
}

