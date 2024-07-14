#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>

#define COLOR_RESET   "\x1b[0m"
#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"
#define COLOR_WHITE   "\x1b[37m"


// Function to set the terminal to non-canonical mode
void setNonCanonicalMode(int enable) {
    struct termios tty;
    tcgetattr(STDIN_FILENO, &tty);

    if (enable) {
        tty.c_lflag &= ~(ICANON | ECHO); // Disable canonical mode and echo
    } else {
        tty.c_lflag |= (ICANON | ECHO);  // Enable canonical mode and echo
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &tty);
}

// Function to check if a key has been pressed
int kbhit() {
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if(ch != EOF) {
        ungetc(ch, stdin);
        return 1;
    }

    return 0;
}

/* Utility Function */

void clearScreen()
{ 
    system("clear");
}

bool logging = true;

bool plug_matrix[26][26];

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

//Setup Parameter
typedef struct scram_state 
{
    int walzenlage[3];
    int shifts[3];
    char window[3];
    bool notches_engaged[2];
} t_state;

typedef struct connect {
    char in;
    char out;
    int scram_id;
} t_connect;

typedef struct row
{
    int shifts[12];
    t_state states[12];
    t_connect connects[12];
    int num_conn;
    char test_cable;
} t_row;

//Scrambler Functions

/*Plugboard*/
// char S(char in, bool is_logging) {
//     //Setup letter map
//     char letter_map[26];
//     for (int i = 0; i < 26; i++) {
//         letter_map[i] = alphabet[i];
//     }


//     for (int i = 0; i < 20; i += 2) {
//         letter_map[key_sheet.steckerverbindungen[i] - 'A'] = key_sheet.steckerverbindungen[i+1];
//         letter_map[key_sheet.steckerverbindungen[i+1] - 'A'] = key_sheet.steckerverbindungen[i];
//     }
//     if (is_logging) {printf("Plug: %c->%c\n", in, letter_map[in - 'A']);}
//     return letter_map[in - 'A'];
// }

// char S_inv(char in, bool is_logging) {
//     char out = S(in, false);
//     if (is_logging) {printf("Plug: %c->%c\n", in, out);}
//     return out;
// }

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
char N(t_state* state, char in, bool is_logging) {

    //Ceasar Shift For Rotation
    char in_shift = P(in, state->shifts[2], false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[2] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift 
    char out_shift = P_inv(out, state->shifts[2], false);

    //Log and Output
    if (is_logging) {printf("--W: %c->%c\n", in, out_shift);}
    return out_shift;
}

char N_inv(t_state* state, char in, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[2] - 1)];
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
    char in_shift = P(in, state->shifts[1], false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[1] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift 
    char out_shift = P_inv(out, state->shifts[1], false);

    //Log and Output
    if (is_logging) {printf("-W-: %c->%c\n", in, out_shift);}
    return out_shift;
}

char M_inv(t_state* state, char in, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[1] - 1)];
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
    char in_shift = P(in, state->shifts[0], false);

    //Map Letter
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[0] - 1)];
    char out = rotor_mapping[(in_shift - 'A') % sizeof(alphabet)];

    //Reverse Ceasar Shift 
    char out_shift = P_inv(out, state->shifts[0], false);

    //Log and Output
    if (is_logging) {printf("W--: %c->%c\n", in, out_shift);}
    return out_shift;
}

char L_inv(t_state* state, char in, bool is_logging) {
    //Setup letter map
    char *rotor_mapping = rotor[(size_t)(state->walzenlage[0] - 1)];
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

//Cipher Functions

/*Standard Scrambler Encryption*/
void scrambler_reset(t_state *state) {
    //Initialize
    for (int i = 0; i < 3; i++) {
        state->shifts[i] = 0;
        state->window[i] = 'Z';
    }

    //Check Notch Flags
    state->notches_engaged[1] = ('Y'   == state->window[2]);
    state->notches_engaged[0] = ('Y'   == state->window[1]);
}

void scrambler_advance(t_state *state, int steps) {
    for (int i = 0; i < steps; i++) {
        //Move Window and Reset Flags
        state->shifts[0] += 1;
        state->window[0] = P(state->window[0], 1, false);
        if (state->notches_engaged[1] && state->notches_engaged[0]) { 
            state->shifts[2] += 1; 
            state->window[2] = P(state->window[2], 1, false);
            state->shifts[1] += 1; 
            state->window[1] = P(state->window[1], 1, false);
            state->notches_engaged[1] = false;
            state->notches_engaged[0] = false; 
        }
        if (state->notches_engaged[1]) { 
            state->shifts[1] += 1; 
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
}

void row_advance(t_row *row, int steps) {
    for (int i = 0; i < 12; i++) {
        scrambler_advance(&row->states[i], steps);
    }
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

void displayScrambler(char (*mappingFunction)(t_state*, char, bool), t_state *state, bool is_logging) {
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
        printf("%c ", mappingFunction(state, c, is_logging));
    }
    printf("\n");
}

void displayMatrix(bool pm[26][26]) {
    // Print the column headers (a-z)
    printf("  ");
    for (char col = 'a'; col <= 'z'; col++) {
        printf(" %c", col);
    }
    printf("\n");

    // Print the grid with row headers (A-Z)
    for (int i = 0; i < 26; i++) {
        printf("%c ", 'A' + i);  // Print row header
        for (int j = 0; j < 26; j++) {
            printf(" %d", pm[i][j]);
        }
        printf("\n");
    }
}

void displayBombe(bool pm[26][26], t_row row) {
    // Print the column headers (a-z)
    printf("  ");
    for (char col = 'a'; col <= 'z'; col++) {
        printf(COLOR_GREEN " %c" COLOR_RESET, col);
    }
    printf("\n");

    // Print the grid with row headers (A-Z)
    for (int i = 0; i < 26; i++) {
        printf(COLOR_RED "%c " COLOR_RESET, 'A' + i);  // Print row header
        for (int j = 0; j < 26; j++) {
                        if (pm[i][j] == 1) {
                printf(COLOR_MAGENTA " 1" COLOR_RESET);
            } else {
                printf(COLOR_CYAN " %d" COLOR_RESET, pm[i][j]);
            }
        }

        // Display Scramblers

        // First Scrambler Row
        if (i == 0) {
            printf("     ");
            for (int j = 0; j < 12; j++) {
                printf(COLOR_YELLOW " %c" COLOR_RESET, row.states[j].window[0]);
            }
            printf("\t\t\t\t");
            char indicator = row.states[0].window[0] == 'Z' ? 'Z' : 'A' + 'Y' - row.states[0].window[0];
            printf(COLOR_MAGENTA " %c" COLOR_RESET, indicator);
        }
        // Second Scrambler Row
        if (i == 1) {
            printf("     ");
            for (int j = 0; j < 12; j++) {
                printf(COLOR_YELLOW " %c" COLOR_RESET, row.states[j].window[1]);
            }
            printf("\t\t\t\t");
            char indicator = row.states[0].window[1] == 'Z' ? 'Z' : 'A' + 'Y' - row.states[0].window[1];
            printf(COLOR_MAGENTA " %c" COLOR_RESET, indicator);
        } 
        // Third Scrambler Row
        if (i == 2) {
            printf("     ");
            for (int j = 0; j < 12; j++) {
                printf(COLOR_YELLOW " %c" COLOR_RESET, row.states[j].window[2]);
            }
            printf("\t\t\t\t");
            char indicator = P_inv(row.states[0].window[2], row.shifts[0], false) == 'Z' ? 'Z' : 'A' + 'Y' - P_inv(row.states[0].window[2], row.shifts[0], false);
            printf(COLOR_MAGENTA " %c" COLOR_RESET, indicator);
        } 

        // Display Test Register

        if (i == 5) {
            printf("     ");
            for (int j = 'a'; j <= 'z'; j++) {
                printf(COLOR_BLUE " %c" COLOR_RESET, j);
            }
        } 
        if (i == 6) {
            printf("    " COLOR_RED "%c" COLOR_RESET, row.test_cable);
            for (int j = 0; j < 26; j++) {
                if (pm[row.test_cable - 'A'][j] == 1) {
                    printf(COLOR_MAGENTA " 1" COLOR_RESET);
                } else {
                    printf(COLOR_CYAN " %d" COLOR_RESET, pm[row.test_cable - 'A'][j]);
                }
            }
        }
        printf("\n");
    }
}

void displayCable(bool pm[26][26], char cable) {
    // Print the column headers (a-z)
    printf("  ");
    for (char col = 'a'; col <= 'z'; col++) {
        printf(" %c", col);
    }
    printf("\n");

    // Print the grid with row headers (A-Z)
    int i = cable - 'A';
        printf("%c ", cable);  // Print row header
        for (int j = 0; j < 26; j++) {
            printf(" %d", pm[i][j]);
        }
        printf("\n");
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
    diagonal_update(pm);

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
                    if (cout[k] == 0 && update[k] == 1) { /*printf("LIT UP %c%c\n", conn.out, k+'a');*/ updated = true;}
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
                    if (cin[k] == 0 && update[k] == 1) { /*printf("LIT UP %c%c\n", conn.in, k+'a');*/ updated = true;}
                    cable_set(pm, conn.in, k+'a', update[k] || cin[k]);
                }
            }
        }
    }
    
    //Update diagonal matrix
    diagonal_update(pm);

    return updated;
}

int main() {
    // key_sheet.ringstellung[0] = 2;
    // displayRotor(N, logging);
    t_row row = {0};
    row.test_cable = 'G';

    //Create connection between cable A and B via scrambler 1
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

    int shifts[12] = {11, 5, 6, 14, 13, 7, 16, 2, 10, 9, 12, 15};

    for (int i = 0; i < 12; i++) {
        row.states[i].walzenlage[2] = 3;
        row.states[i].walzenlage[1] = 5;
        row.states[i].walzenlage[0] = 2;
        row.shifts[i] = shifts[i];
    }

    row_reset(&row);
    setNonCanonicalMode(1);
    for (int i = 0; i < 26*26*26; i++) {
        // if (i % 1000 == 0) {printf("%d\n", i);}
        plugboard_reset(plug_matrix);
        cable_set(plug_matrix, 'G', 'a', true); 
        while(plugboard_update(plug_matrix, &row)) {}
        clearScreen();
        displayBombe(plug_matrix, row);


        row_advance(&row, 1);

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
            } while (ch != 't');
        }
    }

    // while(true) {

        
    //     row_advance(&row, 1);
    //     char indicator2 = row.states[0].window[0] == 'Z' ? 'Z' : 'A' + 'Y' - row.states[0].window[0];
    //     char indicator1 = row.states[0].window[1] == 'Z' ? 'Z' : 'A' + 'Y' - row.states[0].window[1];
    //     char indicator0 =  P_inv(row.states[0].window[2], row.shifts[0], false) == 'Z' ? 'Z' : 'A' + 'Y' - P_inv(row.states[0].window[2], row.shifts[0], false);

    //     if (indicator0 == 'X' && indicator1 == 'K' && indicator2 == 'D') {break;}
    // }

    // plugboard_reset(plug_matrix);
    //     cable_set(plug_matrix, 'G', 'a', true); 
    //     while(plugboard_update(plug_matrix, &row)) {
    //     displayBombe(plug_matrix, row);
    //     printf("\n\n");
    //     usleep(1000000);
    // }
    // displayBombe(plug_matrix, row);

    return 0;
}
