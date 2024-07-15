#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

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
bool logging = true;

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
    {2, 5, 3}, 
    {4, 11, 24},
    "YWY",
    "UFETGQADVNHMZPLJIKXO"
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
char N(char in, bool is_logging) {

    //Ceasar Shift For Rotation (Considering Ringstellung)
    char in_shift = P(in, 26 + enigma_state.shifts[2]-(key_sheet.ringstellung[2]-1), false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[2] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift (Considering Ringstellung)
    char out_shift = P_inv(out, 26 + enigma_state.shifts[2]-(key_sheet.ringstellung[2]-1), false);

    //Log and Output
    if (is_logging) {printf("--W: %c->%c\n", in, out_shift);}
    return out_shift;
}

char N_inv(char in, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[2] - 1)];
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = N(i + 'A', false);
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
char M(char in, bool is_logging) {

    //Ceasar Shift For Rotation (Considering Ringstellung)
    char in_shift = P(in, 26 + enigma_state.shifts[1]-(key_sheet.ringstellung[1]-1), false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[1] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift (Considering Ringstellung)
    char out_shift = P_inv(out, 26 + enigma_state.shifts[1]-(key_sheet.ringstellung[1]-1), false);

    //Log and Output
    if (is_logging) {printf("-W-: %c->%c\n", in, out_shift);}
    return out_shift;
}

char M_inv(char in, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[1] - 1)];
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = M(i + 'A', false);
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
char L(char in, bool is_logging) {
    //Ceasar Shift For Rotation (Considering Ringstellung)
    char in_shift = P(in, 26 + enigma_state.shifts[0]-(key_sheet.ringstellung[0]-1), false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[0] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift (Considering Ringstellung)
    char out_shift = P_inv(out, 26 + enigma_state.shifts[0]-(key_sheet.ringstellung[0]-1), false);

    //Log and Output
    if (is_logging) {printf("W--: %c->%c\n", in, out_shift);}
    return out_shift;
}

char L_inv(char in, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(key_sheet.walzenlage[0] - 1)];
    char letter_map[26];
    for (int i = 0; i < 26; i++) {
        letter_map[i] = L(i + 'A', false);
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

/*Reflector*/
char R(char in, bool is_logging) {
    char *reflector_mapping = reflector[0];
    if (is_logging) {printf("Refl: %c->%c\n", in, reflector_mapping[(in - 'A')]);}
    return reflector_mapping[(in - 'A')];
}

//Cipher Functions

/*Standard Enigma Encryption*/
void enigma_reset() {
    //Initialize
    for (int i = 0; i < 3; i++) {
        enigma_state.shifts[i] = (key_sheet.spruchschlusse[i] - 'A');
        enigma_state.window[i] = key_sheet.spruchschlusse[i];
    }
        //Check Notch Flags
    enigma_state.notches_engaged[1] = (turnover[key_sheet.walzenlage[2]-1]   == enigma_state.window[2]);
    enigma_state.notches_engaged[0] = (turnover[key_sheet.walzenlage[1]-1]   == enigma_state.window[1]);
}

char enigma_encrypt(char in) {
    //Move Window and Reset Flags
    enigma_state.shifts[2] += 1;
    enigma_state.window[2] = P(enigma_state.window[2], 1, false);
    if (enigma_state.notches_engaged[0]) { 
        enigma_state.shifts[1] += 1; 
        enigma_state.window[1] = P(enigma_state.window[1], 1, false);
        enigma_state.shifts[0] += 1; 
        enigma_state.window[0] = P(enigma_state.window[0], 1, false);
        enigma_state.notches_engaged[1] = false;
        enigma_state.notches_engaged[0]= false; 
    }
    if (enigma_state.notches_engaged[1]) { 
        enigma_state.shifts[1] += 1; 
        enigma_state.window[1] = P(enigma_state.window[1], 1, false);
        enigma_state.notches_engaged[1] = false; 
    }


    //Print Letters in Window
    printf("Shifts : \"%c-%c-%c\"\n", (enigma_state.shifts[0]%26) + 'A', (enigma_state.shifts[1]%26) + 'A', (enigma_state.shifts[2]%26) + 'A');
    if (logging) {printf("Window: %c-%c-%c\n", enigma_state.window[0]
                     , enigma_state.window[1]
                     , enigma_state.window[2]); }

    //Check Notch Flags
    enigma_state.notches_engaged[1] = (turnover[key_sheet.walzenlage[2]-1]   == enigma_state.window[2]);
    enigma_state.notches_engaged[0] = (turnover[key_sheet.walzenlage[1]-1]   == enigma_state.window[1]);
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
                                            , logging)
                                        , logging)
                                    , logging)
                                , logging
                                )
                            , logging)
                        , logging)
                    , logging)
                , logging
                );
}

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




int main() {
    enigma_reset();
    char cipher_text[] = "SNMKGGSTZZUGARLV";
    // key_sheet.ringstellung[0] = 2;
    for(int i = 0; i < strlen(cipher_text); i++) {
    printf("", enigma_encrypt(cipher_text[i]));
    // displayRotor(N, logging);
    }
    // for (int i = 0; i < strlen(cipher_text); i ++) {
    //     char enc =  enigma_encrypt('A');
    //     printf("%c-%c-%c : %c->%c\n",enigma_state.window[0], enigma_state.window[1], enigma_state.window[2], 'A', enc);
    // }
    // return 0;
}