#ifndef TERMINAL_H
#define TERMINAL_H

#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>
#include <stdlib.h>

#define CLEAR_SCREEN  "\x1b[H" 
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
  printf("%s", CLEAR_SCREEN);
}

#endif //TERMINAL_H
