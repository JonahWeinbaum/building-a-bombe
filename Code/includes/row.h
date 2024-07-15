#ifndef ROW_H
#define ROW_H

#include "structs.h"
#include "rotors.h"

bool plug_matrix[26][26];

void scrambler_reset(t_state *state) {
    //Initialize
    for (int i = 0; i < 3; i++) {
        state->shifts[i] = 'Z'-'A';
        state->window[i] = 'Z';
    }

    //Check Notch Flags
    state->notches_engaged[1] = ('Y'   == state->window[0]);
    state->notches_engaged[0] = ('Y'   == state->window[1]);
}

void scrambler_advance(t_state *state, int steps) {
    for (int i = 0; i < steps; i++) {
        //Move Window and Reset Flags
        state->window[0] = P(state->window[0], 1, false);
        if (state->notches_engaged[0]) { 
            state->window[2] = P(state->window[2], 1, false);
            state->window[1] = P(state->window[1], 1, false);
            state->notches_engaged[1] = false;
            state->notches_engaged[0] = false; 
        }
        if (state->notches_engaged[1]) { 
            state->window[1] = P(state->window[1], 1, false);
            state->notches_engaged[1] = false;

        }
        //Check Notch Flags
        state->notches_engaged[1] = ('Y'   == state->window[0]);
        state->notches_engaged[0] = ('Y'   == state->window[1]);
    }
}

char scrambler(t_state* state, char in, bool logging) {

    //Encrypt
    return
            N_inv(state,
                M_inv(state,
                    L_inv(state,
                        R(
                            L(state,
                                M(state,
                                    N(state,
                                        in
                                    , logging)
                                , logging)
                            , logging)
                        , logging)
                    , logging)
                , logging)
            , logging);
}

void row_reset(t_row *row) {
    for (int i = 0; i < 12; i++) {
        scrambler_reset(&row->states[i]);
        row->states[i].window[2] = P(row->states[i].window[2], row->shifts[i], false);
        row->states[i].shifts[2] += row->shifts[i];
       //scrambler_advance(&row->states[i], row->shifts[i]);
    }

    //Add in row failures
    for (int i = 0; i < 12; i++) {
            row->states[i].shifts[0] += 26 - row_fails[row->states[i].walzenlage[0]-1];
            row->states[i].shifts[1] += 26 - row_fails[row->states[i].walzenlage[1]-1];
            row->states[i].shifts[2] += 26 - row_fails[row->states[i].walzenlage[2]-1];
    }
     
    //Update Ringstellung
    char indicator2 = row->states[0].window[0] == 'Z' ? 'Z' : 'A' + 'Y' - row->states[0].window[0];
    char indicator1 = row->states[0].window[1] == 'Z' ? 'Z' : 'A' + 'Y' - row->states[0].window[1];
    char indicator0 =  P_inv(row->states[0].window[2], row->shifts[0], false) == 'Z' ? 'Z' : 'A' + 'Y' - P_inv(row->states[0].window[2], row->shifts[0], false);

    char ring0 = indicator2-'A'+1;
    char ring1 = indicator1-'A'+1;
    char ring2 = indicator0-'A'+1;

    for (int i = 0; i < 12; i++) {
        row->states[i].ringstellung[2] = ring2;
        row->states[i].ringstellung[1] = ring1;
        row->states[i].ringstellung[0] = ring0;
    }
}

void row_advance(t_row *row, int steps) {
    for (int i = 0; i < 12; i++) {
        scrambler_advance(&row->states[i], steps);
    }
    
    //Update Ringstellung
    char indicator2 = row->states[0].window[0] == 'Z' ? 'Z' : 'A' + 'Y' - row->states[0].window[0];
    char indicator1 = row->states[0].window[1] == 'Z' ? 'Z' : 'A' + 'Y' - row->states[0].window[1];
    char indicator0 =  P_inv(row->states[0].window[2], row->shifts[0], false) == 'Z' ? 'Z' : 'A' + 'Y' - P_inv(row->states[0].window[2], row->shifts[0], false);

    char ring2 = indicator0-'A'+1;
    char ring1 = indicator1-'A'+1;
    char ring0 = indicator2-'A'+1;


    for (int i = 0; i < 12; i++) {
        row->states[i].ringstellung[2] = ring2;
        row->states[i].ringstellung[1] = ring1;
        row->states[i].ringstellung[0] = ring0;
    }
}



void cable_set(bool pm[26][26], char cable, char set, bool val) {
    pm[cable-'A'][set-'a'] = val;
}

void diagonal_update(bool pm[26][26]) {
    for (int i = 0; i < 26; i++) {
        for (int j = 0; j < 26; j++) {
            if(pm[i][j]) {
                pm[j][i] = 1;
            }
        }
    }
}

void cable_state(bool pm[26][26], bool cable_state[26], char cable) {
    for (int i = 0; i < 26; i++) {
        cable_state[i] = pm[cable - 'A'][i];
    }
}

void cable_scrambler(bool pm[26][26], bool output_state[26], char cable, t_state *scram) {
    //Get cable state
    bool cs[26];
    cable_state(pm, cs, cable);

    for (char in = 'A'; in <= 'Z'; in++) {
        //If has current, run it through scrambler and update output
        if (cs[in-'A']) {
            //printf("Ringstellung : {%d, %d, %d}\n", scram->ringstellung[0], scram->ringstellung[1], scram->ringstellung[2]);
            //printf("Spruchschlusse : \"%c%c%c\"\n", (scram->shifts[0]%26) + 'A', (scram->shifts[1]%26) + 'A', (scram->shifts[2]%26) + 'A');
            //printf("%c-%c-%c\n", (scram->shifts[0]%26) + 'A', (scram->shifts[1]%26) + 'A', (scram->shifts[2]%26) + 'A');
            char out = scrambler(scram, in, false);
            output_state[out-'A'] = true;
        }
    } 
}

void plugboard_reset(bool pm[26][26]) {
    for (int i = 0; i < 26; i++) {
        for (int j = 0; j < 26; j++) {
            pm[i][j] = 0;
        }
    }
}

bool plugboard_update(bool pm[26][26], t_row *row) {
    bool updated = false;

    //Update diagonal matrix
    //diagonal_update(pm);

    //Send current through each cable
    for (char cable = 'A'; cable <= 'Z'; cable++) {
        //Get cable state 
        bool cs[26], cin[26], cout[26];
        cable_state(pm, cs, cable);

        //Check if any scamblers are connected to cable
        for (int i = 0; i < row->num_conn; i++) {
            t_connect conn = row->connects[i];
            
            //Check scrambler ins
            if (conn.in == cable) {
                //printf("%c CABLE PASSING THROUGH SCRAMBLER (%d, %s)\n", cable, conn.scram_id+1, "in");
                //Get cable state output
                cable_state(pm, cout, conn.out);

                //Run cable through scrambler
                bool update[26] = {0};
                cable_scrambler(pm, update, cable, &(row->states[conn.scram_id]));

                //OR values to update
                for (int k = 0; k < 26; k++) {
                    if (cout[k] == 0 && update[k] == 1) {/*printf("LIT UP %c%c\n", conn.out, k+'a');*/ updated = true;}
                    cable_set(pm, conn.out, k+'a', update[k] || cout[k]);
                }
            }

            //Check scrambler outs
            if (conn.out == cable) {
                //printf("%c CABLE PASSING THROUGH SCRAMBLER (%d, %s)\n", cable, conn.scram_id+1, "out");

                //Get cable state input
                cable_state(pm, cin, conn.in);

                //Run cable through scrambler
                bool update[26] = {0};
                cable_scrambler(pm, update, cable, &(row->states[conn.scram_id]));

                //OR values to update
                for (int k = 0; k < 26; k++) {
                    if (cin[k] == 0 && update[k] == 1) { /*printf("LIT UP %c%c\n", conn.in, k+'a'); */ updated = true;}
                    cable_set(pm, conn.in, k+'a', update[k] || cin[k]);
                }
            }
        }
    }
    
    //Update diagonal matrix
    //diagonal_update(pm);

    return updated;
}

#endif //ROW_H