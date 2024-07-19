#ifndef ENIGMA_H
#define ENIGMA_H

#include "config.h"
#include "rotors.h"

/*Standard Enigma Encryption*/
void enigma_reset() {
    //Initialize
    for (int i = 0; i < 3; i++) {
        enigma_state.ringstellung[0] = key_sheet.ringstellung[0];
        enigma_state.ringstellung[1] = key_sheet.ringstellung[1];
        enigma_state.ringstellung[2] = key_sheet.ringstellung[2];
        enigma_state.walzenlage[0] = key_sheet.walzenlage[0];
        enigma_state.walzenlage[1] = key_sheet.walzenlage[1];
        enigma_state.walzenlage[2] = key_sheet.walzenlage[2];
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
    if (logging) {printf("Window: %c-%c-%c\n", enigma_state.window[0]
                     , enigma_state.window[1]
                     , enigma_state.window[2]); }

    //Check Notch Flags
    enigma_state.notches_engaged[1] = (turnover[key_sheet.walzenlage[2]-1]   == enigma_state.window[2]);
    enigma_state.notches_engaged[0] = (turnover[key_sheet.walzenlage[1]-1]   == enigma_state.window[1]);
    //Encrypt
    return  S_inv(&key_sheet,
                    N_inv(&enigma_state, 
                        M_inv(&enigma_state,
                            L_inv(&enigma_state,
                                R(
                                    L(&enigma_state,
                                        M(&enigma_state, 
                                            N(&enigma_state,
                                                S(&key_sheet, in, logging)
                                            , logging)
                                        , logging)
                                    , logging)
                                , logging
                                )
                            , logging)
                        , logging)
                    , logging)
                , logging);
}


#endif //ENIGMA_H