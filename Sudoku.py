from math import floor
from typing import List, Set
from Field import Field
from random import choice

class Sudoku:
    def __init__(self, board: List[List[int]]):
        self.board = [[Field(i,j) for j in range(9)] for i in range(9)]
        for y in range(9):
            for x in range(9):
                self.board[y][x].setAnchor(board[y][x])

    def __str__(self) -> str:
        out = ""
        for line in self.board:
            for field in line:
                out+= str(field)
            out+="\n"
        return out
    
    def colapse_board(self):
        for line in range(9):
            for col in range(9):
                field:Field = self.board[line][col]
                if not field.final:
                    self.update_entropy(line, col)
                    if field.final:
                        self.colapse_board()
    
    def update_entropy(self, lin, col):
        field:Field = self.board[lin][col]
        if field.final: return field.final
        line = self.get_line(lin)
        column = self.get_column(col)
        quadr = self.get_quadr(lin, col)
        union = line.union(column).union(quadr)
        possibilities = {i for i in range(1,10)}
        field.possible = possibilities.difference(union)
        field.update_state()
            
    def get_line(self, lin) -> Set[int]:
        return {self.board[lin][i].final for i in range(9) if self.board[lin][i].final is not None}
    
    def get_column(self, col) -> Set[int]:
        return {self.board[i][col].final for i in range(9) if self.board[i][col].final is not None}
    
    def get_quadr(self, lin, col) -> Set[int]:
        lin = floor(lin/3)*3
        col = floor(col/3)*3
        out = set()
        for j in range(3):
            out.update({self.board[lin+j][col+i].final for i in range(3)})
        out.discard(None)
        return out

    def get_least_entropy(self) -> List[Field]:
        min_entropy = 10
        out = []
        for line in range(9):
            for col in range(9):
                field:Field = self.board[line][col]
                if field.final: continue
                
                entropy = len(field.possible)
                if entropy == 0:
                    continue
                if entropy == min_entropy:
                    out.append(field)
                elif entropy < min_entropy:
                    out = [field]
                    min_entropy = entropy
        return out
    
    def undo_move(self, line, column) -> None:
        field:Field = self.board[line][column]
        field.final = None
        self.update_entropy(line, column)
        
    def done(self) -> bool:
        for line in range(9):
            for col in range(9):
                field:Field = self.board[line][col]
                if not field.final:
                    return False
        return True 
    
    def fail(self) -> bool:
        for line in range(9):
            for col in range(9):
                field:Field = self.board[line][col]
                if len(field.possible) == 0:
                    return True
        return False 

    def check_solution(self):
        for line in range(9):
            if sum(self.get_line(line)) != 45: 
                return False
            if sum(self.get_column(line)) != 45: 
                return False

        for i in range(3):
            for j in range(3):
                if sum(self.get_quadr(i*3, j*3)) != 45: 
                    return False
        return True
                

        
        
    


        



if __name__ == "__main__":
    TAB =      [[5,3,0,0,7,0,0,0,0],
                [6,0,0,1,9,5,0,0,0],
                [0,9,8,0,0,0,0,6,0],
                [8,0,0,0,6,0,0,0,3],
                [4,0,0,8,0,3,0,0,1],
                [7,0,0,0,2,0,0,0,6],
                [0,6,0,0,0,0,2,8,0],
                [0,0,0,4,1,9,0,0,5],
                [0,0,0,0,8,0,0,7,9]]
    game = Sudoku(TAB)

    print(game)
    print(game.get_quadr(0,6))
    game.colapse_board()

    print(game)
    print(game.check_solution())
    print("OK")
        