# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:28:53 2020

@author: User
"""

import pandas as pd
import time
from math import floor
import numpy as np

def duplicados(data):
    if type(data) == pd.Series:
        indexes = list(data.index)
        out = []
        for i in indexes:
            valor = data[i] # valor a ser analisado
            analisar = indexes.copy()
            analisar.remove(i)
            for j in analisar:
                if data[j] == valor:
                    out.append(j)
        return data[out]
    
    if type(data) == pd.DataFrame:
        out = []
        out2 = pd.DataFrame(index=data.index, columns=data.columns)
        changed = False
        for coluna in data:
            for linha in data[coluna].index:
                valor = data[coluna][linha] #coordenadas e valor do obj atual
                data2 = data.copy()
                data2[coluna][linha] == 0
                
                for coluna2 in data2:
                    for linha2 in data2[coluna2].index:
                        if coluna2 == coluna and linha2 == linha:
                            continue
                        
                        valor2 = data2[coluna2][linha2]
                        if valor2 == valor:
                            dic = {(linha, coluna) : valor}
                            #if not(dic in out):
                            out.append(dic)
                            out2[coluna][linha] = valor
                            changed = True
        if changed:
            return out2


class game:
    
    def __init__(self, tabuleiro):
        self.tab = pd.DataFrame(tabuleiro, dtype='object')
        
        
    def get_quadrante(self, linha, coluna):
        y = floor(coluna/3)
        x = floor(linha/3)
        a = 3*x
        b = 3*y
        
        return self.tab.loc[[0+a,1+a,2+a],[0+b,1+b,2+b]]
        
    
    def get_quadrantes_values(self, linha, coluna):
        x = floor(coluna/3)
        y = floor(linha/3)
        
        def quadrante(x, y):
            a = 3*x
            b = 3*y
            return self.tab.loc[[0+a,1+a,2+a],[0+b,1+b,2+b]]
        
        def valores_quadrantes(quadr):
            valores = []
            for i in quadr.values:
                for a in i:
                    valores.append(a)
            
            return valores
        
        return pd.Series(valores_quadrantes(quadrante(y, x)))


    def get_linha(self, linha):
        return self.tab.iloc[linha]


    def get_coluna(self, coluna):
        return self.tab[coluna]
    
    
    def check(self, valores):
        
        def strip_valores(quadr):
            valores = []
            for i in quadr.values:
                try:
                    for a in i:
                        valores.append(a)
                except:
                    valores.append(i)
            
            return valores
        
        duplicados = strip_valores(valores).duplicated()
        n_duplicados = len(duplicados[duplicados==True])
        
        if n_duplicados == 0:
            return True
        else:
            return False
        
    
    def valores_posiveis(self, linha, coluna): # refazer direito
        def func(x): #criterio
            if not x in range(1,10):
                return False
            else:
                return True
        
        valores_linha = self.get_linha(linha)[self.get_linha(linha).apply(func)]
        valores_coluna = self.get_coluna(coluna)[self.get_coluna(coluna).apply(func)]
        valores_quadr = self.get_quadrantes_values(linha, coluna)[self.get_quadrantes_values(linha, coluna).apply(func)]
        a = pd.concat([valores_coluna, valores_linha, valores_quadr]).drop_duplicates()
        out = list(range(1,10))
        for valor in a.values:
            out.remove(valor)
        return out


    def solve_step(self):
        
        def naked_pairs(coluna, linha):
            linha_duplas = self.get_linha(linha)[ self.get_linha(linha).apply(
                lambda x: True if type(x) == list and len(x) == 2 else False)]
            
            coluna_duplas = self.get_coluna(coluna)[ self.get_coluna(coluna).apply(
                lambda x: True if type(x) == list and len(x) == 2 else False)]
            
            quadrante_duplas = self.get_quadrante(linha, coluna)
            a = []
            for i in quadrante_duplas:
                a.append(quadrante_duplas[i][quadrante_duplas[i].apply(
                    lambda x: True if type(x) == list and len(x) == 2 else False)])
            quadrante_duplas = pd.concat(a, axis=1)
            
            
            quadrante_duplas = duplicados(quadrante_duplas)
            linha_duplas = duplicados(linha_duplas)
            coluna_duplas = duplicados(coluna_duplas)
            
            if len(quadrante_duplas) != 0:
                pass
            
        def checar_possibilidades():
            """
            checar se só existe um numero possivel para a celula dentre as possibilidades
            das demais celualas do mesmo grupo
            """
            
            return "triangulo"
            
            
        
        for coluna in self.tab.columns: # coluna [0,9]
            for linha in self.tab.index: # linha [0,9]
                cell = self.tab.at[linha, coluna]
                if type(cell) == int and cell != 0:
                    continue
                
                possibilidades = self.valores_posiveis(linha, coluna)
                if len(possibilidades) == 1: #se só tiver uma possibilidade
                    self.tab.at[linha, coluna] = possibilidades[0]
                    continue
                    
                elif cell != possibilidades:
                    self.tab.at[linha, coluna] = possibilidades
                
        return self.tab

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
        
jogo = game(TAB2)
for i in range(10):
    jogo.solve_step()

jogo.valores_posiveis(6,4)

