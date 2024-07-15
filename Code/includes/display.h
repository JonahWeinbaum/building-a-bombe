#ifndef DISPLAY_H
#define DISPLAY_H

#include <stdio.h>
#include "terminal.h"
#include "ceasar.h"
#include "row.h"

void displayCeasar(char (*mappingFunction)(char, int, bool), int deg, bool is_logging) {
    // Print the top row (A to Z)
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("%c ", c);
    }
    printf("\n");

    // Print the mapping arrows
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("| ");
    }
    printf("\n");

    // Print the bottom row (mapped characters)
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("%c ", mappingFunction(c, deg, is_logging));
    }
    printf("\n");
}

void displayCable(bool pm[26][26], char cable) {
    // Print the column headers (a-z)
    printf("  ");
    for (char col = 'a'; col <= 'z'; col++) {
        printf(" %c", col);
    }
    printf("\n");

    // Print the grid with row headers (A-Z)
    int i = cable - 'A';
        printf("%c ", cable);  // Print row header
        for (int j = 0; j < 26; j++) {
            printf(" %d", pm[i][j]);
        }
        printf("\n");
}

void displayBombe(bool pm[26][26], t_row row) {
    // Print the column headers (a-z)
    printf("  ");
    for (char col = 'a'; col <= 'z'; col++) {
        printf(COLOR_GREEN " %c" COLOR_RESET, col);
    }
    printf("\n");

    // Print the grid with row headers (A-Z)
    for (int i = 0; i < 26; i++) {
        printf(COLOR_RED "%c " COLOR_RESET, 'A' + i);  // Print row header
        for (int j = 0; j < 26; j++) {
                        if (pm[i][j] == 1) {
                printf(COLOR_MAGENTA " 1" COLOR_RESET);
            } else {
                printf(COLOR_CYAN " %d" COLOR_RESET, pm[i][j]);
            }
        }

        // Display Scramblers

        // First Scrambler Row
        if (i == 0) {
            printf("     ");
            for (int j = 0; j < 12; j++) {
                printf(COLOR_YELLOW " %c" COLOR_RESET, row.states[j].window[0]);
            }
            printf("\t\t\t\t");
            char indicator = row.states[0].window[0] == 'Z' ? 'Z' : 'A' + 'Y' - row.states[0].window[0];
            printf(COLOR_MAGENTA " %c" COLOR_RESET, indicator);
        }
        // Second Scrambler Row
        if (i == 1) {
            printf("     ");
            for (int j = 0; j < 12; j++) {
                printf(COLOR_YELLOW " %c" COLOR_RESET, row.states[j].window[1]);
            }
            printf("\t\t\t\t");
            char indicator = row.states[0].window[1] == 'Z' ? 'Z' : 'A' + 'Y' - row.states[0].window[1];
            printf(COLOR_MAGENTA " %c" COLOR_RESET, indicator);
        } 
        // Third Scrambler Row
        if (i == 2) {
            printf("     ");
            for (int j = 0; j < 12; j++) {
                printf(COLOR_YELLOW " %c" COLOR_RESET, row.states[j].window[2]);
            }
            printf("\t\t\t\t");
            char indicator = P_inv(row.states[0].window[2], row.shifts[0], false) == 'Z' ? 'Z' : 'A' + 'Y' - P_inv(row.states[0].window[2], row.shifts[0], false);
            printf(COLOR_MAGENTA " %c" COLOR_RESET, indicator);
        } 

        // Display Test Register

        if (i == 5) {
            printf("     ");
            for (int j = 'a'; j <= 'z'; j++) {
                printf(COLOR_BLUE " %c" COLOR_RESET, j);
            }
        } 
        if (i == 6) {
            printf("    " COLOR_RED "%c" COLOR_RESET, row.test_cable);
            for (int j = 0; j < 26; j++) {
                if (pm[row.test_cable - 'A'][j] == 1) {
                    printf(COLOR_MAGENTA " 1" COLOR_RESET);
                } else {
                    printf(COLOR_CYAN " %d" COLOR_RESET, pm[row.test_cable - 'A'][j]);
                }
            }
        }
        printf("\n");
    }
}

void displayRotor(char (*mappingFunction)(char, bool), bool is_logging) {
    // Print the top row (A to Z)
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("%c ", c);
    }
    printf("\n");

    // Print the mapping arrows
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("| ");
    }
    printf("\n");

    // Print the bottom row (mapped characters)
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("%c ", mappingFunction(c, is_logging));
    }
    printf("\n");
}

void displayScrambler(char (*mappingFunction)(t_state*, char, bool), t_state *state, bool is_logging) {
    // Print the top row (A to Z)
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("%c ", c);
    }
    printf("\n");

    // Print the mapping arrows
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("| ");
    }
    printf("\n");

    // Print the bottom row (mapped characters)
    for (char c = 'A'; c <= 'Z'; c++) {
        printf("%c ", mappingFunction(state, c, is_logging));
    }
    printf("\n");
}

void displayMatrix(bool pm[26][26]) {
    // Print the column headers (a-z)
    printf("  ");
    for (char col = 'a'; col <= 'z'; col++) {
        printf(" %c", col);
    }
    printf("\n");

    // Print the grid with row headers (A-Z)
    for (int i = 0; i < 26; i++) {
        printf("%c ", 'A' + i);  // Print row header
        for (int j = 0; j < 26; j++) {
            printf(" %d", pm[i][j]);
        }
        printf("\n");
    }
}

#endif //DISPLAY_H