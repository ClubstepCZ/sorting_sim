import json
import os
import re

# paths for this script
DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, "src")

# reserved names (built-in)
RES_ALG = {
    "Bubble Sort": "bubble_sort",
    "Heap Sort": "heap_sort",
    "Insertion Sort": "insertion_sort",
    "Merge Sort": "merge_sort",
    "Quick Sort": "quick_sort",
    "Selection Sort": "selection_sort"
}

ALG_F = os.path.join(DIR, "algorithms.json")

def v_alg_n(n):
    """This function tests if algorithm name is valid. 
    (name is not empty, can be casted to folder name)"""

    # is empty
    if not n or not n.strip():
        return False

    # max length
    if len(n) > 20:
        return False

    # cannot be valid folder name
    if not re.match(r'^[a-zA-Z0-9_ ]+$', n):
        return False
    if n[0].isdigit():
        return False

    return True

def txt_2_fld(txt):
    """This function converts newly created
    algorithm name to the folder name."""

    return txt.lower().replace(" ", "_")

def ld_alg():
    """This function loads user created algorithms from JSON file"""

    if not os.path.exists(ALG_F):
        return []

    try:
        with open(ALG_F, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        return []

def sv(algs):
    """This function saves user created algorithms to JSON file"""

    with open(ALG_F, 'w') as f:
        json.dump(algs, f, indent=4)

def res(n):
    """This function checks if the given algoritm name 
    (created by user) is in reserved names (built-in)
    """

    for rn, rf in RES_ALG.items():
        
        if (n.lower() == rn.lower() or # could cause folder conflicts
            txt_2_fld(n) == rf):
            return True
    return False

def dup(n, e_algs):
    """This function checks if the given algoritm name 
    (created by user) has already been created (by user)
    """

    f = txt_2_fld(n)

    for alg in e_algs:
        if (n.lower() == alg["name"].lower() or # could cause folder conflicts
            f == alg["folder"].lower()):
            return True
    return False

def cr_alg_dir(f):
    """This function is responsible for 
    creating file structure for new algorithm.
    """

    dir = os.path.join(SRC, f)

    try:
        os.makedirs(dir, exist_ok=False)
        return True
    except FileExistsError:
        return False
    except Exception as e:
        return False

def cr_mf(f):
    """This function is responsible for creating 
    makefile within the folder path of the new algorithm.
    """

    mfp = os.path.join(SRC, f, "Makefile")

    mfc = f"""TARGET := $(notdir $(shell pwd)).so
SRC := $(wildcard *.c)
SRC += ../elementary_ops.c ../memory_tracker.c
OBJ := $(SRC:.c=.o)
CC := gcc
CFLAGS := -std=c11 -fPIC -Wall -Wextra -O2
LDFLAGS := -shared

all: $(TARGET)

$(TARGET): $(OBJ)
\t$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
\t$(CC) $(CFLAGS) -c $< -o $@

clean:
\trm -f $(OBJ) $(TARGET)
"""
    try:
        with open(mfp, 'w') as f:
            f.write(mfc.strip())
        return True
    except Exception as e:
        return False

def cr_cf(f, ep):
    """This function generates users created algorithm C file"""

    cp = os.path.join(SRC, f, f"{f}.c")

    cfc = f"""#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "../memory_tracker.h"
#include "../elementary_ops.h"

/*
 * Use the following macros instead of standard C constructs:
 *
 *  - FOR(init, cond, update)       instead of: for (init; cond; update)
 *  - IF(condition)                 instead of: if (condition)
 *  - WHILE(condition)              instead of: while (condition)
 *  - SWAP(a, b, temp)              instead of: swapping two variables
 *  - TRACK_CHANGE(index)           to track manual changes in array
 *  - ADD(a, b), SUBTRACT(a, b), MULTIPLY(a, b), DIVIDE(a, b)
 *                                  instead of: a + b, a - b, a * b, a / b
 *
 * For recursion, use:
 *  - CALL_FUNCTION_VOID(fn, ...)   instead of: fn(...)
 *  - CALL_FUNCTION_RETURN(fn, ...) instead of: return fn(...)
 *
 * These macros ensure correct counting of elementary operations,
 * memory usage, and enable proper visualization.
 */

void {ep}(int *arr, int n); // Function declaration

void {ep}(int *arr, int n) {{
    set_sorting_array(arr);
    // TODO: Implement your algorithm here
}}
"""
    try:
        with open(cp, 'w') as f:
            f.write(cfc)
        return True
    except Exception as e:
        return False