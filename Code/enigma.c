
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

bool logging = false;

//Static Enigma Wirings 
//Data from https://www.cryptomuseum.com/crypto/enigma/wiring.htm#14
char alphabet[26] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

/* Enigma I Wirings */
char rotor[5][26]={
    /*I*/   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
	/*II*/  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
	/*III*/ "BDFHJLCPRTXVZNYEIWGAKMUSQO",
	/*IV*/  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
	/*V*/   "VZBRGITYUPSDNHLXAWMJQOFECK" 
};

char turnover[5]="QEVJZ";

char reflector[1][26]={
    /*B*/ "YRUHQSLDPXNGOKMIEBFZCWVJAT"
};  

//Setup Parameters
typedef struct parameters
{
  int walzenlage[3];
  int ringstellung[3];
  char spruchschlusse[3];
  char steckerverbindungen[20];
} t_parameters;

t_parameters key_sheet = {
    {1, 2, 5}, 
    {1, 1, 1},
    "AAA",
    ""
    //"POMLIUKJNHYTGBVFREDC"
};

typedef struct eng_state 
{
    int shifts[3];
    char window[3];
    bool notches_engaged[2];
} t_state;

t_state enigma_state;

//Rotor Functions

/*Plugboard*/
char S(char in, bool is_logging) {
    //Setup letter map
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = alphabet[i];
    }


    for (int i = 0; i < 20; i += 2) {
        letter_map[key_sheet.steckerverbindungen[i] - 'A'] = key_sheet.steckerverbindungen[i+1];
        letter_map[key_sheet.steckerverbindungen[i+1] - 'A'] = key_sheet.steckerverbindungen[i];
    }
    if (is_logging) {printf("Plug: %c->%c\n", in, letter_map[in - 'A']);}
    return letter_map[in - 'A'];
}

char S_inv(char in, bool is_logging) {
    char out = S(in, false);
    if (is_logging) {printf("Plug: %c->%c\n", in, out);}
    return out;
}

/* Ceasar Shift*/
char P(char in, int deg, bool is_logging) {
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
            return i + 'A';
        }
    }
    return in;
}

/*First Rotor*/
char N(char in, int shift, bool is_logging) {
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[2] - 1)];
    char rm = rotor_mapping[(in - 'A' + shift) % sizeof(alphabet)];
    if (is_logging) {printf("--W: %c->%c\n", in, P(rm, key_sheet.ringstellung[2] - 1, false));}
    return P(rm, key_sheet.ringstellung[2] - 1, false);
}

char N_inv(char in, int shift, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[2] - 1)];
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = N(i + 'A', shift, false);
    }

    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {
            if (is_logging) {printf("--W: %c->%c\n", in, i + 'A');}
            return i + 'A';
        }
    }
    return in;
}

/*Second Rotor*/
char M(char in, int shift, bool is_logging) {
    //Shift input by inverse of prior rotor shift
    char in_new = P(in, (26 - enigma_state.shifts[2] % sizeof(alphabet)), false);
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[1] - 1)];
    char rm = rotor_mapping[(in_new - 'A' + shift) % sizeof(alphabet)];
    if (is_logging) {printf("-W-: %c->%c\n", in, P(rm, key_sheet.ringstellung[1] - 1, false));}
    return P(rm, key_sheet.ringstellung[1] - 1, false);
}

char M_inv(char in, int shift, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[1] - 1)];
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = M(i + 'A', shift, false);
    }

    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {
            if (is_logging) {printf("-W-: %c->%c\n", in, i + 'A');}
            return i + 'A';
        }
    }
    return in;
}

/*Third Rotor*/
char L(char in, int shift, bool is_logging) {
    char in_new = P(in, (26 - enigma_state.shifts[1] % sizeof(alphabet)), false);
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[0] - 1)];
    char rm = rotor_mapping[(in_new - 'A' + shift) % sizeof(alphabet)];
    if (is_logging) {printf("W--: %c->%c\n", in, P(rm, key_sheet.ringstellung[0] - 1, false));}
    return P(rm, key_sheet.ringstellung[0] - 1, false);
}

char L_inv(char in, int shift, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[0] - 1)];
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = L(i + 'A', shift, false);
    }

    for (int i = 0; i < 26; i++) {
        if (letter_map[i] == in) {
            if (is_logging) {printf("W--: %c->%c\n", in, i + 'A');}
            return i + 'A';
        }
    }
    return in;
}
/*Reflector*/
char R(char in, bool is_logging) {
    char *reflector_mapping = reflector[0];
    if (is_logging) {printf("Refl: %c->%c\n", in, reflector_mapping[(in - 'A')]);}
    return reflector_mapping[(in - 'A')];
}

//Cipher Functions

/*Standard Enigma Encryption*/
void enigma_reset() {
    //Check Notch Flags
    enigma_state.notches_engaged[1] = ((turnover[key_sheet.walzenlage[1]-1] - 'A' + key_sheet.ringstellung[1] - 1) % sizeof(alphabet) + 'A'  == enigma_state.window[2]);
    enigma_state.notches_engaged[0] = ((turnover[key_sheet.walzenlage[0]-1] - 'A' + key_sheet.ringstellung[0] - 1) % sizeof(alphabet) + 'A' == enigma_state.window[1]);
    
    for (int i = 0; i < 3; i++) {
        enigma_state.shifts[i] = 0;
        enigma_state.window[i] = key_sheet.spruchschlusse[i];
    }
}

char enigma_encrypt(char in) {
    //Move Window and Reset Flags
    enigma_state.shifts[2] += 1;
    enigma_state.window[2] = P(enigma_state.window[2], 1, false);
    if (enigma_state.notches_engaged[1]) { 
        enigma_state.shifts[1] += 1; 
        enigma_state.window[1] = P(enigma_state.window[1], 1, false);
        enigma_state.notches_engaged[1] = false; 
    }
    if (enigma_state.notches_engaged[0]) { 
        enigma_state.shifts[0] += 1; 
        enigma_state.window[0] = P(enigma_state.window[0], 1, false);
        enigma_state.notches_engaged[0] = false; 
    }

    //Print Letters in Window
    if (logging) {printf("%c-%c-%c\n", enigma_state.window[0]
                     , enigma_state.window[1]
                     , enigma_state.window[2]); }

    //Check Notch Flags
    enigma_state.notches_engaged[1] = ((turnover[key_sheet.walzenlage[1]-1] - 'A' + key_sheet.ringstellung[1] - 1) % sizeof(alphabet) + 'A'  == enigma_state.window[2]);
    enigma_state.notches_engaged[0] = ((turnover[key_sheet.walzenlage[0]-1] - 'A' + key_sheet.ringstellung[0] - 1) % sizeof(alphabet) + 'A' == enigma_state.window[1]);

    //Encrypt
    return  S_inv(
                    N_inv(
                        M_inv(
                            L_inv(
                                R(
                                    L(
                                        M(
                                            N(
                                                S(in, logging)
                                            , enigma_state.shifts[2], logging)
                                        , enigma_state.shifts[1], logging)
                                    , enigma_state.shifts[0], logging)
                                , logging
                                )
                            , enigma_state.shifts[0], logging)
                        , enigma_state.shifts[1], logging)
                    , enigma_state.shifts[2], logging)
                , logging
                );
}


int main() {
    enigma_reset();
    for (int i = 0; i < 4; i ++) {
        printf("Lamp: %c\n", enigma_encrypt('A'));
    }
    return 0;
}
