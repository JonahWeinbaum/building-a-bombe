# Compiler and flags
CC = gcc
CFLAGS = -Iincludes -Wall -Wextra -Werror

# Directories
SOURCE_DIR = src
OUTPUT_DIR = out

# Source and executable files
SOURCES = $(SOURCE_DIR)/bombe.c
EXECUTABLE = $(OUTPUT_DIR)/bombe

# Default target
all: $(EXECUTABLE)

# Link the executable
$(EXECUTABLE): $(SOURCES)
	@mkdir -p $(OUTPUT_DIR)
	$(CC) $(CFLAGS) $(SOURCES) -o $(EXECUTABLE)

# Clean up build files
clean:
	rm -rf $(OUTPUT_DIR)

# Phony targets
.PHONY: all clean
