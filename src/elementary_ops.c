#include "elementary_ops.h"

size_t element_op_cnt = 0;
swap_callback_t swap_callback = NULL;
change_callback_t change_callback = NULL;
int *global_array = NULL;

void set_sorting_array(int *arr) {
    global_array = arr;
}

void reset_operation_count() {
    element_op_cnt = 0;
}

size_t get_operation_count() {
    return element_op_cnt;
}

void set_swap_callback(swap_callback_t callback) {
    swap_callback = callback;
}

void set_change_callback(change_callback_t callback) {
    change_callback = callback;
}

void record_swap(size_t i, size_t j) {
    //printf("record_swap called with indices %zu and %zu\n", i, j);
    if (swap_callback) {
        //printf("Calling swap callback\n");
        swap_callback(i, j);
    } else {
        //printf("swap_callback is NULL!\n");
    }
}

void record_change(size_t i) {
    //printf("record_change called with index %zu\n", i);
    if (change_callback) {
        //printf("Calling change callback\n");
        change_callback(i, global_array[i]);
    } else {
        //printf("change_callback is NULL!\n");
    }
}