#include <stddef.h>
#include <stdio.h>
#include "../elementary_ops.h"
#include "../memory_tracker.h"

void heapify(int *arr, int n, int i) {
    int largest = i;

    WHILE(1) {
        int left = MULTIPLY(2, largest) + 1;
        int right = MULTIPLY(2, largest) + 2;
        int next = largest;

        IF(left < n && arr[left] > arr[next]) {
            next = left;
        }
        IF(right < n && arr[right] > arr[next]) {
            next = right;
        }

        IF(next == largest) {
            break;
        }

        int temp;
        SWAP(arr[largest], arr[next], temp);
        largest = next;
    }
}

void heap_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);

    FOR(int i = n / 2 - 1, i >= 0, i--) {
        CALL_FUNCTION_VOID(heapify, arr, n, i);
    }

    FOR(int i = n - 1, i > 0, i--) {
        int temp;
        SWAP(arr[0], arr[i], temp);
        CALL_FUNCTION_VOID(heapify, arr, i, 0);
    }
}
