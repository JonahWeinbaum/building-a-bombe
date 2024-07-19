#include "wirings.h"
#include "display.h"
#include "row.h"
#include "structs.h"
#include <stdbool.h>
#include <stdio.h>

char permutation(char input) {
    // Simple example: cycle through 'A' to 'D'
    switch(input) {
        case 'A': return 'B';
        case 'B': return 'C';
        case 'C': return 'D';
        case 'D': return 'A';
        default: return input; // Identity for all other chars
    }
}

void find_cycles(char (*perm_func)(char, t_row*), t_row* loop) {
    bool visited[sizeof(alphabet)] = {false};
    char domain[sizeof(alphabet)];

    // Initialize the domain
    for (size_t i = 0; i < sizeof(alphabet); i++) {
        domain[i] = alphabet[i];
    }

    // Find and print cycles
    for (size_t i = 0; i < sizeof(alphabet); i++) {
        if (!visited[i]) {
            char start = domain[i];
            char current = start;
            printf("(");
            do {
                printf("%c ", current);
                visited[(unsigned char)current-'A'] = true;
                current = perm_func(current, loop);
            } while (current != start);
            printf(")\n");
        }
    }
}

char perm_function(char in, t_row* loop) {
    for (int i = 0; i < loop->num_conn; i++) {
        in = scrambler(&(loop->states[i]), in, false);
    }
    in = scrambler(&(loop->states[0]), in, false);
    return in;
}

int main() {
    t_row loop = {0};

    int shifts[12] = {5, 10, 7, 2, 12, 11, 9, 1, 13, 15, 16, 8};

    for (int i = 0; i < 12; i++) {
        loop.states[i].walzenlage[2] = 3;
        loop.states[i].walzenlage[1] = 5;
        loop.states[i].walzenlage[0] = 2;
        loop.shifts[i] = shifts[i];
    }

    loop.test_cable = 'G';

    loop.num_conn = 3;

    t_connect connect = {0};
    connect.in = 'G';
    connect.out = 'E';
    connect.scram_id = 0;
    loop.connects[0] = connect;

    connect.in = 'E';
    connect.out = 'Q';
    connect.scram_id = 1;
    loop.connects[1] = connect;

    connect.in = 'Q';
    connect.out = 'G';
    connect.scram_id = 2;
    loop.connects[2] = connect;

    // connect.in = 'R';
    // connect.out = 'A';
    // connect.scram_id = 3;
    // loop.connects[3] = connect;


    // connect.in = 'A';
    // connect.out = 'B';
    // connect.scram_id = 4;
    // loop.connects[4] = connect;


    // connect.in = 'B';
    // connect.out = 'D';
    // connect.scram_id = 5;
    // loop.connects[5] = connect;


    // connect.in = 'D';
    // connect.out = 'P';
    // connect.scram_id = 6;
    // loop.connects[6] = connect;


    // connect.in = 'P';
    // connect.out = 'N';
    // connect.scram_id = 7;
    // loop.connects[7] = connect;

    // connect.in = 'N';
    // connect.out = 'M';
    // connect.scram_id = 8;
    // loop.connects[8] = connect;

    // connect.in = 'M';
    // connect.out = 'W';
    // connect.scram_id = 9;
    // loop.connects[9] = connect;

    // connect.in = 'W';
    // connect.out = 'V';
    // connect.scram_id = 10;
    // loop.connects[10] = connect;

    // connect.in = 'V';
    // connect.out = 'G';
    // connect.scram_id = 11;
    // loop.connects[11] = connect;

    row_reset(&loop);

    setNonCanonicalMode(1);
    for (int i = 0; i < 1000; i++) {
        plugboard_reset(plug_matrix);
        cable_set(plug_matrix, 'G', 'b', true); 
        while(plugboard_update(plug_matrix, &loop)) {}
        

        clearScreen();
        displayBombe(plug_matrix, loop); 

        //Reset Terminal Canonical Mode
        find_cycles(perm_function, &loop);

            bool cs[26];
        cable_state(plug_matrix, cs, 'G');

        int sum = 0; 
        for(int l = 0; l < 26; l++) {
            sum += cs[l];
        }
        if (sum == 26) { 
            char ch;
            do {
                ch = getchar();
            } while (ch != 'c');   
        }

                    char ch;
            do {
                ch = getchar();
            } while (ch != 't');   

        row_advance(&loop, 1);
    }
    return 0;
}