#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "../memory_tracker.h"
#include "../elementary_ops.h"

void merge(int *arr, int left, int mid, int right) {
    int n1 = ADD(SUBTRACT(mid, left), 1);
    int n2 = SUBTRACT(right, mid);

    int *left_arr = (int *)malloc(MULTIPLY(n1, sizeof(int)));
    int *right_arr = (int *)malloc(MULTIPLY(n2, sizeof(int)));

    FOR(int i = 0, i < n1, i++) {
        left_arr[i] = arr[ADD(left, i)];
    }
    FOR(int j = 0, j < n2, j++) {
        right_arr[j] = arr[ADD(mid + 1, j)];
    }

    int i = 0, j = 0, k = left;
    WHILE(i < n1 && j < n2) {
        IF(left_arr[i] <= right_arr[j]) {
            arr[k] = left_arr[i];
            TRACK_CHANGE(k);
            i++;
        } else {
            arr[k] = right_arr[j];
            TRACK_CHANGE(k);
            j++;
        }
        k++;
    }

    WHILE(i < n1) {
        arr[k++] = left_arr[i++];
        TRACK_CHANGE(k - 1);
    }
    WHILE(j < n2) {
        arr[k++] = right_arr[j++];
        TRACK_CHANGE(k - 1);
    }

    free(left_arr);
    free(right_arr);
}

void merge_sort(int *arr, int left, int right) {
    IF(left < right) {
        int mid = ADD(left, DIVIDE(SUBTRACT(right, left), 2));
        CALL_FUNCTION_VOID(merge_sort, arr, left, mid);
        CALL_FUNCTION_VOID(merge_sort, arr, ADD(mid, 1), right);
        CALL_FUNCTION_VOID(merge, arr, left, mid, right);
    }
}

void merge_sort_entry_point(int *arr, int n) {
    set_sorting_array(arr);
    CALL_FUNCTION_VOID(merge_sort, arr, 0, n-1);
}