TARGET := $(notdir $(shell pwd)).so
SRC := $(wildcard *.c)
SRC += ../elementary_ops.c ../memory_tracker.c
OBJ := $(SRC:.c=.o)
CC := gcc
CFLAGS := -std=c11 -fPIC -Wall -Wextra -O2
LDFLAGS := -shared

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)