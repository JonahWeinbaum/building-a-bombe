# Compiler and flags
CC = gcc
CFLAGS = -Iincludes -Wall -Wextra -Werror -O3

# Directories
SOURCE_DIR = src
OUTPUT_DIR = out


# Source and executable files
BOMBE_SOURCE = $(SOURCE_DIR)/bombe.c
ENIGMA_SOURCE = $(SOURCE_DIR)/enigma.c
BOMBE_EXECUTABLE = $(OUTPUT_DIR)/bombe
ENIGMA_EXECUTABLE = $(OUTPUT_DIR)/enigma


# Default target
all: $(BOMBE_EXECUTABLE) $(ENIGMA_EXECUTABLE)

# Link the bombe executable
$(BOMBE_EXECUTABLE): $(BOMBE_SOURCE)
	@mkdir -p $(OUTPUT_DIR)
	$(CC) $(CFLAGS) $(BOMBE_SOURCE) -o $(BOMBE_EXECUTABLE)

# Link the enigma executable
$(ENIGMA_EXECUTABLE): $(ENIGMA_SOURCE)
	@mkdir -p $(OUTPUT_DIR)
	$(CC) $(CFLAGS) $(ENIGMA_SOURCE) -o $(ENIGMA_EXECUTABLE)

# Clean up build files
clean:
	rm -rf $(OUTPUT_DIR)

# Phony targets
.PHONY: all clean
