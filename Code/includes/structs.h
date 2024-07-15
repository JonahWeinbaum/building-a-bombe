#ifndef STRUCTS_H
#define STRUCTS_H


//Setup Parameter
typedef struct scram_state 
{
    int walzenlage[3];
    int shifts[3];
    char window[3];
    int ringstellung[3];
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


#endif //STRUCTS_H