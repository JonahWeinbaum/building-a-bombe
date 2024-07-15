#ifndef ROTORS_H
#define ROTORS_H

#include <stdio.h>
#include <stdbool.h>
#include "wirings.h"
#include "ceasar.h"
#include "structs.h"

/*First Rotor*/
char N(t_state* state, char in, bool is_logging) {

    //Ceasar Shift For Rotation
    char in_shift = P(in, 26 + state->shifts[2]-(state->ringstellung[2]-1), false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[2] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift 
    char out_shift = P_inv(out, 26 + state->shifts[2]-(state->ringstellung[2]-1), false);

    //Log and Output
    if (is_logging) {printf("--W: %c->%c\n", in, out_shift);}
    return out_shift;
}

char N_inv(t_state* state, char in, bool is_logging) {
    //Setup letter map
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = N(state, i + 'A', false);
    }

    //Find Letter in Map
    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {

            //Log and Output
            if (is_logging) {printf("--W: %c->%c\n", in, i + 'A');}
            return i + 'A';
        }
    }
    
    //Letter Map Failure
    return -1;
}

/*Second Rotor*/
char M(t_state* state, char in, bool is_logging) {

    //Ceasar Shift For Rotation
    char in_shift = P(in, 26 + state->shifts[1]-(state->ringstellung[1]-1), false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[1] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift 
    char out_shift = P_inv(out, 26 + state->shifts[1]-(state->ringstellung[1]-1), false);

    //Log and Output
    if (is_logging) {printf("-W-: %c->%c\n", in, out_shift);}
    return out_shift;
}

char M_inv(t_state* state, char in, bool is_logging) {
    //Setup letter map
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = M(state, i + 'A', false);
    }

    //Find Letter in Map
    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {

            //Log and Output
            if (is_logging) {printf("-W-: %c->%c\n", in, i + 'A');}
            return i + 'A';
        }
    }
    
    //Letter Map Failure
    return -1;
}


/*Third Rotor*/
char L(t_state* state, char in, bool is_logging) {

    //Ceasar Shift For Rotation
    char in_shift = P(in, 26 + state->shifts[0]-(state->ringstellung[0]-1), false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[0] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift 
    char out_shift = P_inv(out, 26 + state->shifts[0]-(state->ringstellung[0]-1), false);

    //Log and Output
    if (is_logging) {printf("W--: %c->%c\n", in, out_shift);}
    return out_shift;
}

char L_inv(t_state* state, char in, bool is_logging) {
    //Setup letter map
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = L(state, i + 'A', false);
    }

    //Find Letter in Map
    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {

            //Log and Output
            if (is_logging) {printf("W--: %c->%c\n", in, i + 'A');}
            return i + 'A';
        }
    }
    
    //Letter Map Failure
    return -1;
}


/*Reflector*/
char R(char in, bool is_logging) {
    char *reflector_mapping = reflector[0];
    if (is_logging) {printf("Refl: %c->%c\n", in, reflector_mapping[(in - 'A')]);}
    return reflector_mapping[(in - 'A')];
}

#endif //ROTORS_H