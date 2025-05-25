#include <stddef.h>
#include "../elementary_ops.h"
#include "../memory_tracker.h"

int partition(int arr[], int low, int high);
void quick_sort(int arr[], int low, int high);

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = SUBTRACT(low, 1);

    FOR(int j = low, j < high, j++) {
        IF(arr[j] <= pivot) {
            i = ADD(i, 1);
            int temp;
            SWAP(arr[i], arr[j], temp);
        }
    }
    int temp;
    SWAP(arr[ADD(i, 1)], arr[high], temp);
    return ADD(i, 1);
}

void quick_sort(int *arr, int low, int high) {
    set_sorting_array(arr);
    IF(low < high) {
        int pi = CALL_FUNCTION_RETURN(partition, arr, low, high);
        CALL_FUNCTION_VOID(quick_sort, arr, low, SUBTRACT(pi, 1));
        CALL_FUNCTION_VOID(quick_sort, arr, ADD(pi, 1), high);
    }
}

void quick_sort_entry_point(int *arr, int n) {
    CALL_FUNCTION_VOID(quick_sort, arr, 0, n-1);
}