#ifndef ELEMENTARY_OPS_H
#define ELEMENTARY_OPS_H

#include <stddef.h>
#include <stdio.h>

extern size_t element_op_cnt;
typedef void (*swap_callback_t)(size_t, size_t);
typedef void (*change_callback_t)(size_t, int);

extern swap_callback_t swap_callback;
extern change_callback_t change_callback;
extern int *global_array;

void set_sorting_array(int *arr);
void reset_operation_count();
size_t get_operation_count();
void set_swap_callback(swap_callback_t callback);
void set_change_callback(change_callback_t callback);

void record_swap(size_t i, size_t j);
void record_change(size_t i);

#define FOR(start, condition, increment) \
        for (start; (condition) && (++element_op_cnt, 1); (increment, ++element_op_cnt))

#define IF(condition) \
    if ((condition) && (++element_op_cnt, 1))

#define WHILE(condition) \
    while ((condition) && (++element_op_cnt, 1))

#define SWAP(a, b, temp) \
    do { \
        temp = (a); \
        (a) = (b); \
        (b) = temp; \
        element_op_cnt += 3; \
        if (global_array) { \
            size_t idx_a = (&(a) - global_array); \
            size_t idx_b = (&(b) - global_array); \
            record_swap(idx_a, idx_b); \
        } \
    } while (0)

#define TRACK_CHANGE(idx) \
    do { \
        element_op_cnt++; \
        if (global_array) { \
            size_t _idx = (size_t)(&(global_array[idx]) - global_array); \
            record_change(_idx); \
        } \
    } while (0)


#define ADD(a, b) ({ element_op_cnt++; (a) + (b); })
#define SUBTRACT(a, b) ({ element_op_cnt++; (a) - (b); })
#define MULTIPLY(a, b) ({ element_op_cnt++; (a) * (b); })
#define DIVIDE(a, b) ({ element_op_cnt++; (a) / (b); })

#endif
