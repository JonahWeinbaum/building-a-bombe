#ifndef WIRINGS_H
#define WIRINGS_H

#include "structs.h"
#include <stdbool.h>

char alphabet[26] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

//Static Enigma Wirings 
//Data from https://www.cryptomuseum.com/crypto/enigma/wiring.htm#14

/*
The drums have similar wiring as their Enigma counterparts but there are differences. 
Probably by mistake, drums I, II, III, VI, VII and VIII on the Bombe are one letter ahead of the corresponding Enigma rotors. 
Drum IV is two steps ahead, and rotor V is three steps ahead. 
*/

/* Enigma I Wirings */
char rotor[5][26]={
    /*I*/   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
	/*II*/  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
	/*III*/ "BDFHJLCPRTXVZNYEIWGAKMUSQO",
	/*IV*/  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
	/*V*/   "VZBRGITYUPSDNHLXAWMJQOFECK" 
};

char turnover[5]="QEVJZ";

int row_fails[5] = {1, 1, 1, 2, 3};

char reflector[1][26]={
    /*B*/ "YRUHQSLDPXNGOKMIEBFZCWVJAT"
};  

bool plug_matrix[26][26];

t_state enigma_state;

#endif //WIRINGS_H