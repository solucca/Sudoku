# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 18:05:14 2020

@author: User
"""
import pygame
import pandas as pd
from tabuleiro import game

class janela:
    def __init__(self, tabuleiro):
        self.tab = tabuleiro
        pygame.init()
        self.white = (255, 255, 255)
        self.black = (0,0,0)
        self.size = (900, 900)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('SUDOKU')
        self.screen.fill(self.white)
        self.myFont = pygame.font.SysFont("Arial", 60)
        
        self.draw_lines()
        self.draw_numbers()
        self.jogo = game(self.tab)
        
    def draw_lines(self):
        w, h = self.size
        linha_grossa = 6
        linha_fina = 3
        
        pygame.draw.line(self.screen, self.black, (w/3, 0), (w/3, h), linha_grossa)
        pygame.draw.line(self.screen, self.black, (2*w/3, 0), (2*w/3, h), linha_grossa)
        
        pygame.draw.line(self.screen, self.black, (0, h/3), (w, h/3), linha_grossa)
        pygame.draw.line(self.screen, self.black, (0, 2*h/3), (w, 2*h/3), linha_grossa)
        
        for i in range(1, 9): #de 1 a 9
            y = int(i*h/9)
            x = int(i*w/9)
            pygame.draw.line(self.screen, self.black, (0, y), (w, y), linha_fina)
            pygame.draw.line(self.screen, self.black, (x, 0), (x, h), linha_fina)
            
    def draw_numbers(self):
        for coluna in self.tab.columns:
            for linha in self.tab.index:
                valor = self.tab[coluna][linha]
                if valor == 0 or type(valor) != int:
                    continue
                self.draw_number(linha, coluna, valor)
            
    def draw_number(self, linha, coluna, numero):
        w, h = self.size
        text = self.myFont.render(str(numero), True, self.black)
        tw = text.get_width()
        th = text.get_height()
        self.screen.blit(text, (coluna*w/9 + w/18 - tw/2, linha*h/9 + h/18 -th/2))
        
    
    def update(self):
        self.tab = self.jogo.solve_step()
        self.screen.fill(self.white)
        self.draw_numbers()
        self.draw_lines()
        
        
    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print('certo')
                        self.update()
                    
            pygame.display.flip()
        pygame.quit()


TAB1 =      [[5,3,0,0,7,0,0,0,0],
             [6,0,0,1,9,5,0,0,0],
             [0,9,8,0,0,0,0,6,0],
             [8,0,0,0,6,0,0,0,3],
             [4,0,0,8,0,3,0,0,1],
             [7,0,0,0,2,0,0,0,6],
             [0,6,0,0,0,0,2,8,0],
             [0,0,0,4,1,9,0,0,5],
             [0,0,0,0,8,0,0,7,9]]

TAB2 =      [[0,0,0,0,8,0,0,7,0],
             [0,4,0,2,0,7,0,0,0],
             [0,0,7,0,0,3,5,4,9],
             [2,0,0,0,0,0,3,0,0],
             [0,0,6,0,3,0,0,0,0],
             [7,0,0,0,9,6,0,8,0],
             [3,0,0,5,0,1,0,2,8],
             [1,8,0,4,0,0,0,6,3],
             [0,6,0,0,0,0,4,0,0]]

tabuleiro = pd.DataFrame(TAB2, dtype='object')

teste = janela(tabuleiro)
teste.run()


