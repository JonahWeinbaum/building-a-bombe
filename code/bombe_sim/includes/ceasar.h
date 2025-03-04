#ifndef CEASAR_H
#define CEASAR_H

#include "wirings.h"

/* Ceasar Shift*/
char P(char in, int deg, bool is_logging) {
    if (is_logging) { printf("Shift %d: %c -> %c\n", deg, in, alphabet[(in - 'A' + deg) % sizeof(alphabet)]); }
    return alphabet[(in - 'A' + deg) % sizeof(alphabet)];
}

char P_inv(char in, int deg, bool is_logging) {
    //Setup letter map
    char letter_map[26];
    
    for (int i = 0; i < 26; i++) {
        letter_map[i] = P(i + 'A', deg, false);
    }

    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {
            if (is_logging) { printf("Shift %d: %c -> %c\n", deg, in, i+'A'); }
            return i + 'A';
        }
    }

    return in;
}

#endif //CEASAR_H