#ifndef MEMORY_TRACKER_H
#define MEMORY_TRACKER_H

#include <stddef.h>
#include "elementary_ops.h"
#include <stdio.h>

typedef struct {
    void* ptr;
    size_t size;
} allocation_record;

size_t get_peak_stack_usage();
void reset_peak_stack_usage();

#define malloc(size) track_malloc(size)
#define free(ptr) track_free(ptr)

void* track_malloc(size_t size);
void track_free(void* ptr);
size_t get_peak_memory_usage();
void reset_peak_memory_usage();
extern size_t get_stack_pointer();

extern size_t current_recursion_depth;
extern size_t max_recursion_depth;

#define CALL_FUNCTION_VOID(fn, ...) \
    do { \
        current_recursion_depth++; \
        if (current_recursion_depth > max_recursion_depth) \
            max_recursion_depth = current_recursion_depth; \
        \
        element_op_cnt++; \
        fn(__VA_ARGS__); \
        \
        current_recursion_depth--; \
    } while (0)

#define CALL_FUNCTION_RETURN(fn, ...) \
    ({ \
        current_recursion_depth++; \
        if (current_recursion_depth > max_recursion_depth) \
            max_recursion_depth = current_recursion_depth; \
        \
        element_op_cnt++; \
        __typeof__(fn(__VA_ARGS__)) _result = fn(__VA_ARGS__); \
        \
        current_recursion_depth--; \
        _result; \
    })

#endif