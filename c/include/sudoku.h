#include <stdint.h>
#include <stdbool.h>

#define EMPTY 0 // there is no number filled in this field yet
#define FULL_ENTROPY 0x03FE // all numbers are equally likely (bits 1-9 are set to 1)

// Represents a field in the Sudoku Board
typedef struct
{
    uint8_t value;    // What number is inside of this Field, 0 if no value was determined yet
    uint16_t entropy; // What possible numbers could exist here
    uint8_t energy;   // The number of possible states (how many possible numers) 
    uint8_t x;        // X Coordinate in the Sudoku board
    uint8_t y;        // Y Coordinate in the Sudoku board
} field_t;


// Represents a Soduku board
typedef struct
{
    field_t fields[81]; // Each Field (Line1)(Line2)...(Line9)
    bool solved;        // If the board is solved or not
    uint8_t n_completed;
    uint8_t energy;     // if energy is 0 board is in end state (not necessarly solved)
} board_t;


/**
 * Generates a board from the input file
 */
board_t generate_board(char *input);


/**
 * Prints the values of the board to stdout
 */
void print_board(board_t *board);


/**
 * Prints the energy value of each field in a board
 */
void print_energy(board_t *board);

/**
 * Sets the entropy of a specific field.
 * Sets the n-th bit to 1 or 0 depending on value
*/
void set_entropy(field_t *field, uint8_t digit, uint8_t value);


/**
 * Calculates the entropy of all fields in a board
*/
void update_entropy(board_t *board);

/* Solves a Sudoku Board :) */
bool solve(board_t *board);

/** Calculates the entropy of a Field in a specific position by looking 
 * the numbers around and in the same quadrant
 * If energy is 1 by the end of calculation, then colapse into that state
*/
void calculate_entropy(board_t* board, uint8_t x, uint8_t y);

/** Calculates the energy on a specific Field*/
uint8_t get_energy(field_t* field);

// returns a pointer to the field in the board containing the lowest entropy
field_t* get_lowest_energy(board_t* board);

//colapses a field into one of its possible states and returns what state it colapsed into
uint8_t collapse(field_t* field);

//gets a field with given x and y values
field_t* get_field(board_t* board, uint8_t x, uint8_t y);

void simple_solve_loop(board_t *board);

/** Checks if solution is right*/
bool check_solution(board_t* board);