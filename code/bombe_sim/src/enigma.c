#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "enigma.h"

int main() {
    enigma_reset();
    char cipher_text[] = "JJJWSSAKFIGEBTPAYC";
    for(size_t i = 0; i < strlen(cipher_text); i++) {
        printf("%c", enigma_encrypt(cipher_text[i]));
    }

    return 0;
}

// XAZ XAZ THEORYREADINGGROUP
// VCO YUP JJJWSSAKFIGEBTPAYC