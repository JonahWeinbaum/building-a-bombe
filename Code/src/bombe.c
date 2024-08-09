#include <stdio.h>
#include <stdbool.h>
#include "wirings.h"
#include "terminal.h"
#include "display.h"
#include "ceasar.h"

int main() {
    //Set Terminal to Non-Canonical Mode
    setNonCanonicalMode(1);

    bool include_diagonal = true;

    t_row row = {0};

    int shifts[12] = {11, 5, 6, 14, 13, 7, 16, 2, 10, 9, 12, 15};

    for (int i = 0; i < 12; i++) {
        row.states[i].walzenlage[2] = 3;
        row.states[i].walzenlage[1] = 5;
        row.states[i].walzenlage[0] = 2;
        row.shifts[i] = shifts[i];
    }

    row.test_cable = 'G';

    row.num_conn = 12;

    t_connect connect = {0};
    connect.in = 'U';
    connect.out = 'E';
    connect.scram_id = 0;
    row.connects[0] = connect;

    connect.in = 'E';
    connect.out = 'G';
    connect.scram_id = 1;
    row.connects[1] = connect;

    connect.in = 'G';
    connect.out = 'R';
    connect.scram_id = 2;
    row.connects[2] = connect;

    connect.in = 'R';
    connect.out = 'A';
    connect.scram_id = 3;
    row.connects[3] = connect;

    connect.in = 'A';
    connect.out = 'S';
    connect.scram_id = 4;
    row.connects[4] = connect;

    connect.in = 'S';
    connect.out = 'V';
    connect.scram_id = 5;
    row.connects[5] = connect;

    connect.in = 'V';
    connect.out = 'E';
    connect.scram_id = 6;
    row.connects[6] = connect;

    connect.in = 'E';
    connect.out = 'N';
    connect.scram_id = 7;
    row.connects[7] = connect;

    connect.in = 'H';
    connect.out = 'Z';
    connect.scram_id = 8;
    row.connects[8] = connect;

    connect.in = 'Z';
    connect.out = 'R';
    connect.scram_id = 9;
    row.connects[9] = connect;

    connect.in = 'R';
    connect.out = 'G';
    connect.scram_id = 10;
    row.connects[10] = connect;

    connect.in = 'G';
    connect.out = 'L';
    connect.scram_id = 11;
    row.connects[11] = connect;

    row_reset(&row);
    for (int i = 0; i < 26*26*26; i++) {
        plugboard_reset(plug_matrix);
        cable_set(plug_matrix, 'G', 'a', true); 
        while(plugboard_update(plug_matrix, &row, include_diagonal)) {}
        
            // char ch;
            // do {
            //     ch = getchar();
            // } while (ch != 'c');   

        clearScreen();
        displayBombe(plug_matrix, row); 
        usleep(10000);
        row_advance(&row, 1);

        char ch;
        do {
            ch = getchar();
        } while (ch != 'n'); 

        bool cs[26];
        cable_state(plug_matrix, cs, 'G');

        int sum = 0; 
        for(int l = 0; l < 26; l++) {
            sum += cs[l];
        }
        if (sum != 26) { 
            char ch;
            do {
                ch = getchar();
            } while (ch != 'c');   
        }
    }

    //Reset Terminal Canonical Mode
    setNonCanonicalMode(0);

    return 0;
}
