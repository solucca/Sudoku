#include <stdlib.h>
#include <stdio.h>
#include "include/sudoku.h"

int main(int argc, char *argv[]){
    // char *test = "026030008"
    //              "900600100"
    //              "000019040"
    //              "007302000"
    //              "004070800"
    //              "000806700"
    //              "050720000"
    //              "009005004"
    //              "400060210";
    char *board_string;
    if( argc == 2 ) {
        board_string = argv[1];
    }
    else{
        board_string =  "100570300"
                        "000000570"
                        "600090008"
                        "000000041"
                        "000000000"
                        "728000000"
                        "090206000"
                        "000001203"
                        "352000900";
    }
   
    board_t board = generate_board(board_string);
    simple_solve_loop(&board);
    print_board(&board);
    solve(&board);
    printf("Solution %d\n", check_solution(&board));
}