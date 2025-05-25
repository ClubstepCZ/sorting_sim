#include <stddef.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "memory_tracker.h"

#define MAX_STACK_SIZE 10000
static allocation_record allocation_stack[MAX_STACK_SIZE];
static size_t stack_top = 0;

size_t current_recursion_depth = 0;
size_t max_recursion_depth = 0;

static size_t current_memory_usage = 0;
static size_t peak_memory_usage = 0;

void* track_malloc(size_t size) {
    void* ptr = __builtin_malloc(size);
    if (ptr && stack_top < MAX_STACK_SIZE) {
        allocation_stack[stack_top].ptr = ptr;
        allocation_stack[stack_top].size = size;
        stack_top++;
        
        current_memory_usage += size;
        if (current_memory_usage > peak_memory_usage) {
            peak_memory_usage = current_memory_usage;
        }
    }
    return ptr;
}

void track_free(void* ptr) {
    if (!ptr) return;
    
    // LIFO order
    for (size_t i = stack_top; i > 0; i--) {
        if (allocation_stack[i-1].ptr == ptr) {
            current_memory_usage -= allocation_stack[i-1].size;
            __builtin_free(ptr);
            
            // Shift remaining elements down
            if (i < stack_top) {  // Only needed if not freeing top element
                memmove(&allocation_stack[i-1], &allocation_stack[i],
                       (stack_top - i) * sizeof(allocation_record));
            }
            stack_top--;
            return;
        }
    }
    
    // Not found on the stack
    __builtin_free(ptr);
}

size_t get_peak_memory_usage() {
    return peak_memory_usage;
}

void reset_peak_memory_usage() {
    peak_memory_usage = 0;
    current_memory_usage = 0;
    stack_top = 0;
}

void reset_stack_usage() {
    current_recursion_depth = 0;
    max_recursion_depth = 0;
}

size_t get_peak_stack_usage() {
    return max_recursion_depth;
}

void reset_peak_stack_usage() {
    max_recursion_depth = 0;
    current_recursion_depth = 0;
}