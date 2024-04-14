#include "include/sudoku.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


board_t generate_board(char* input){
    board_t board;
    board.n_completed = 0;
    for (int i = 0; i < 81; i++){
        field_t field;
        field.value = (uint16_t)*input - 48;
        field.x = i % 9;
        field.y = i / 9;
        if (field.value == EMPTY) {
            field.entropy = FULL_ENTROPY;
            field.energy = 9;
        }
        else {
            board.n_completed++;
            field.entropy = 0;
            field.energy = 0;
        }
        board.fields[i] = field;
        input++;
    }
    board.solved = false;
    return board;
}


void print_board(board_t* board){
    printf("--- Board: %d ---\n\n", board->n_completed);
    for (int i = 0; i < 9; i++){
        printf(" ");
        for (int j = 0; j < 9; j ++){
            if (j%3 == 0 && j != 0) printf("│ ");
            if (board->fields[i*9+j].value)
                printf("\033[0;32m%d\033[0m ", board->fields[i*9+j].value);
            else
                printf("\033[0;31m%d\033[0m ", board->fields[i*9+j].energy);
            // else
            //     printf("☐ ");
        }
        if ((i+1)%3 == 0 && i != 8) printf("\n───────┼───────┼───────");
        printf("\n");
    }
    printf("\n");
}


void print_energy(board_t* board){
    for (int i = 0; i < 9; i++){
        for (int j = 0; j < 9; j ++){
            printf("%d ", board->fields[i*9+j].energy);
        }
        printf("\n");
    }
}

// this function sets the entropy
void set_entropy(field_t *field, uint8_t digit, uint8_t value){
    if (value) {
        field->entropy |= (1 << digit);
    } else {
        field->entropy &= ~(1 << digit);
    }
    field->energy = get_energy(field);
    // We must check all possibilities before setting the field
    // if (field->energy == 1){
    //     uint16_t value = field->entropy;
    //     for (int i = 0; i < 16; i++) {
    //         if (value & (1 << i)) {
    //             field->value = i;
    //             field->energy = 0;
    //             field->entropy = 0;
    //             break;
    //         }
    //     }
    // }
}


void update_entropy(board_t* board){
    board->n_completed = 0;
    board->energy = 0;
    for (int x = 0; x < 9; x++) {
        for (int y = 0; y < 9; y++) {
            calculate_entropy(board, x, y);
            field_t* field = get_field(board, x,y);
            if (field->energy == 1){ // if only one possible state, then colapse
                uint16_t value = field->entropy;
                for (int i = 0; i < 16; i++) {
                    if (value & (1 << i)) {
                        field->value = i;
                        field->energy = 0;
                        field->entropy = 0;
                        break;
                    }
                }
            }
            board->energy += get_energy(field);
            if (field->value) board->n_completed++;
        }
    }
    board->solved = (board->n_completed == 81);
}

void simple_solve_loop(board_t *board){
    if (board->solved) return;
    uint8_t last_filled = board->n_completed;
    update_entropy(board);
    while (board->n_completed > last_filled){
        last_filled = board->n_completed;
        update_entropy(board);
    }
}

uint8_t get_num_of_lowest_states(board_t *board){
    field_t *lowest = get_lowest_energy(board);
    uint8_t counter = 0;
    for (uint8_t i = 0; i < 81; i++){
        if (board->fields[i].energy == lowest->energy)
            counter++;
    }
    return counter;
}

board_t* copy_board_n_times(const board_t* board, size_t n) {
    // Allocate memory for n board_t structures
    board_t* copies = malloc(n * sizeof(board_t));
    if (copies == NULL) {
        perror("Failed to allocate memory");
        exit(EXIT_FAILURE);
    }

    // Copy data from the original board to each copy
    for (size_t i = 0; i < n; ++i) {
        copies[i] = *board; // Copy the entire structure
    }

    return copies;
}

uint8_t* get_list_lowest_energy(board_t* board){
    uint8_t n = get_num_of_lowest_states(board);
    uint8_t min_energy = get_lowest_energy(board)->energy;
    uint8_t* list = malloc(n*sizeof(uint8_t));
    uint8_t c = 0;
    for (uint8_t i = 0; i < 81; i++){
        field_t* field = &(board->fields[i]);
        // there is no energy lower than 2
        if (field->energy == min_energy){
            list[c] = i;
            c++;
        }
    }
    return list;
}

bool solve(board_t *board){
    simple_solve_loop(board);
    if (board->energy == 0 || board->solved) 
        return board->solved;
    
    /* Strategy:
       ---------
        - We create a checkpoint for each of field in lowest state
        - Explore run simple solve on each checkpoint
        - Continue execution where we got further
            (?) Save checkpoint to return in case no solution found in branch (?)
            We are using loops, that means we have no backtrace because of recurison
            So in order to go back in case of loose end we save the path as a list of 
            coordinates that were set in each loop    
        */
    
    uint16_t counter = 0;
    uint8_t max_steps = 81 - board->n_completed;
    uint8_t *path = malloc(max_steps*sizeof(uint8_t)); // what fields were 'guessed' on each iteration
    while (board->solved == false && counter < 500){
        uint8_t n_to_explore = get_num_of_lowest_states(board);
        board_t* to_explore = copy_board_n_times(board, n_to_explore);
        // now we need a list of the indexes of the lowest states:
        uint8_t* index_lowest_energies = get_list_lowest_energy(board);
        // and a list of n_completed by table after colapse
        uint8_t *n_completed = (uint8_t*) malloc(n_to_explore*sizeof(uint8_t));
        for (uint8_t i = 0; i < n_to_explore; i++){
            field_t* lowest = &(to_explore+i)->fields[*(index_lowest_energies+i)];
            collapse(lowest);
            simple_solve_loop(to_explore+i);
            *(n_completed+i) = (to_explore+i)->n_completed;
        }
        // \/ TODO: Create new list instead! I will still need the data of what field was colapsed 
        // index_lowest_energies <- now is a list of number of completed, get the board with highest.
        uint8_t max = 0;
        uint8_t index = 0;
        for (uint8_t i = 0; i < n_to_explore; i++){
            if ((to_explore+i)->n_completed > max ){
                max = (to_explore+i)->n_completed;
                index = i;
            }
        }
        *board = *(to_explore+index);
        free(index_lowest_energies);
        free(to_explore);
        if (board->solved)
            return true;
        counter++;
    }
    free(path);
    return board->solved;


    // while (!board->solved){
    //     board_t checkpoint = *board;
    //     field_t* lowest = get_lowest_energy(board);

    //     uint8_t digit = collapse(lowest);
    //     board->n_completed++;
    //     solve(board, depth + 1);
    //     if (board->solved) return board->solved;

    //     // return to checkpoint and rule out failed state
    //     *board = checkpoint;
    //     set_entropy(get_field(board, lowest->x, lowest->y), digit, 0);
    //     // try to simply solve the board using simple method
    //     simple_solve_loop(board);
    //     if (board->solved)
    //         return true;
    //     if (board->energy == 0) 
    //         return false;
    // }
    // return false;
}

uint8_t collapse(field_t* field){
    uint16_t entropy = field->entropy >> 1;
    uint8_t digit = 1;
    while (entropy){
        if (entropy & 1) {
            field->value = digit;
            field->energy = 0;
            field->entropy = 0;
            return digit;
        } 
        entropy >>=1;
        digit++;
    }
    return -1;
}

field_t* get_lowest_energy(board_t* board){
    uint8_t min_energy = 0xFF;
    uint8_t min_index = 0;
    for (uint8_t i = 0; i < 81; i++){
        field_t* field = &(board->fields[i]);
        // there is no energy lower than 2
        if (field->energy == 2) return field;
        // update lowest energy
        if (field->energy < min_energy && field->value == 0){
            min_energy = field->energy; 
            min_index = i;
        }
    }
    return &(board->fields[min_index]);
}


/** Calculates the energy on a specific Field*/
uint8_t get_energy(field_t* field){
    uint8_t count = 0;
    uint16_t value = field->entropy;
    while (value) {
        count += value & 1;
        value >>= 1;
    }
    return count;
}


/** Gets the field in a specific coordinate*/
field_t* get_field(board_t* board, uint8_t x, uint8_t y){
    return &(board->fields[y*9+x]);
}


/** Calculates the entropy of a Field in a specific position by looking 
 * the numbers around and in the same quadrant
 * If energy is 1 by the end of calculation, then colapse into that state
*/
void calculate_entropy(board_t* board, uint8_t x, uint8_t y){
    field_t* target = get_field(board, x, y);
    if (target->value != 0) return;
    // check line
    for (uint8_t var_x = 0; var_x < 9; var_x++){
        field_t* field = get_field(board, var_x, y);
        if (target == field) continue;
        if (field->value != 0) set_entropy(target, field->value, 0);
    }
    // check column
    for (uint8_t var_y = 0; var_y < 9; var_y++){
        field_t* field = get_field(board, x, var_y);
        if (target == field) continue;
        if (field->value != 0) set_entropy(target, field->value, 0);
    }
    // check quadrants
    uint8_t qx = (x/3)*3;
    uint8_t qy = (y/3)*3;
    for (uint8_t var_x = qx; var_x < qx+3; var_x++){
        for (uint8_t var_y = qy; var_y < qy+3; var_y++){
            if (var_x == x || var_y == y ) continue;
            field_t* field = get_field(board, var_x, var_y);
            if (field->value != 0) set_entropy(target, field->value, 0);
        }
    }
}

/** Checks if a board was correctly solved*/
bool check_solution(board_t* board){
    if (!board->solved) return false;
    if (board->energy != 0) return false;
    uint8_t seen[9] = {0,0,0,0,0,0,0,0,0};
    // check line and column
    for (uint8_t i = 0; i < 9; i++){
        // check line
        for (uint8_t x = 0; x < 9; x++){
            uint8_t digit = board->fields[i*9+x].value-1;
            if (seen[digit]) 
                return false;
            seen[digit] = 1;
        }
        for (int i = 0; i < 9; i++) seen[i] = 0;

        // check column
        for (uint8_t x = 0; x < 9; x++){
            uint8_t digit = board->fields[x*9+i].value-1;
            if (seen[digit]) 
                return false;
            seen[digit] = 1;
        }
        for (int i = 0; i < 9; i++) seen[i] = 0;
    }
    
    // check quadrants
    uint8_t t = 0;
    for (uint8_t q = 0; q < 81; q += 3){
        seen[board->fields[q].value-1]++;seen[board->fields[q+1].value-1]++;seen[board->fields[q+2].value-1]++;
        seen[board->fields[q+9].value-1]++;seen[board->fields[q+10].value-1]++;seen[board->fields[q+11].value-1]++;
        seen[board->fields[q+18].value-1]++;seen[board->fields[q+19].value-1]++;seen[board->fields[q+20].value-1]++;
        for (uint8_t j = 0; j < 9; j++)
            if (seen[j] != 1) 
                return false;
        for (uint8_t j = 0; j < 9; j++) seen[j] = 0;
        t++;
        if (t==3){
            t = 0;
            q += 18;
        } 
    }
    return true;
}
