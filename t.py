# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo ??:
# 103369 Miguel Parece
# 99970 João Maçãs

import sys
import random
import copy
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class Board:

    def __init__(self,row_counts,col_counts,) -> None:
        self.board = [['0' for _ in range(10)] for _ in range(10)]
        self.row_counts = row_counts
        self.col_counts = col_counts
        self.initialHints = []
        self.hintedShips = []
        self.shipsLeft = [4,3,2,1]

    def noHintedShips(self):
        return True if not self.hintedShips else False

    def updateInitialHints(self):
        for hint in self.initialHints:
            row,col,value = hint
            self.board[row][col] = value

    def hintsEmpty(self):
        for i in range(10):
            if self.col_counts[i]!=0:
                return False
            if self.row_counts[i]!=0:
                return False
        return True

    def noShipsLeft(self):
        for i in range(4):
            if self.shipsLeft[i] != 0:
                return False
        return True

    def updateSurroundOfAction(self,action):
        row,col,value,size = action

        if size==1:
            if row!=0:
                self.board[row-1][col]='.'
                if col!=0:
                    self.board[row-1][col-1]='.'
                if col!=9:
                    self.board[row-1][col+1]='.'
            if row != 9:
                self.board[row+1][col]='.'
                if col!=9:
                    self.board[row+1][col+1]='.'
                if col!=0:
                    self.board[row+1][col-1]='.'
            if col!= 9:
                self.board[row][col+1]='.'
            if col != 0:
                self.board[row][col-1]='.'
            return

        if value=='l':
            for i in range(size):
                if i==0:
                    if row!=9:
                        self.board[row+1][col]='.'
                        if col!=0:
                            self.board[row+1][col-1]='.'
                    if row!=0:
                        self.board[row-1][col]='.'
                        if col!=0:
                            self.board[row-1][col-1]='.'
                    if col!=0:
                        self.board[row][col-1]='.'
                
                elif i==size-1:
                    if row!=9:
                        self.board[row+1][col+i]='.'
                        if col+i!=9:
                            self.board[row+1][col+1+i]='.'
                    if row!=0:
                        self.board[row-1][col+i]='.'
                        if col+i!=9:
                            self.board[row-1][col+1+i]='.'
                    if col+i!=9:
                        self.board[row][col+1+i]='.'

                else:
                    if row!=9:
                        self.board[row+1][col+i]='.'
                    if row!=0:
                        self.board[row-1][col+i]='.'
            
            return

        if value=='t':
            for i in range(size):
                if i==0:
                    if col!=9:
                        self.board[row][col+1]='.'
                        if row!=0:
                            self.board[row-1][col+1]='.'
                    if col!=0:
                        self.board[row][col-1]='.'
                        if row!=0:
                            self.board[row-1][col-1]='.'
                    if row!=0:
                        self.board[row-1][col]='.'
                
                elif i==size-1:
                    if col!=9:
                        self.board[row+i][col+1]='.'
                        if row+i!=9:
                            self.board[row+1+i][col+1]='.'
                    
                    if col!=0:
                        self.board[row+i][col-1]='.'
                        if row+i!=9:
                            self.board[row+1+i][col-1]='.'
                    if row+i!=9:
                        self.board[row+1+i][col]='.'

                else:
                    if col!=9:
                        self.board[row+i][col+1]='.'
                    if row!=0:
                        self.board[row+i][col-1]='.'

            return
        
        print('ERROR SurroundedAction')
        return

    def updateSurroundOfCell(self,cell):
        row,col,value = cell
        min_coord = 0
        max_coord=9
        if value=='c':
            if row!=0:
                self.board[row-1][col]='.'
                if col!=0:
                    self.board[row-1][col-1]='.'
                if col!=9:
                    self.board[row-1][col+1]='.'
            if row != 9:
                self.board[row+1][col]='.'
                if col!=9:
                    self.board[row+1][col+1]='.'
                if col!=0:
                    self.board[row+1][col-1]='.'
            if col!= 9:
                self.board[row][col+1]='.'
            if col != 0:
                self.board[row][col-1]='.'
            
        if value=='l':
            if row!=9:
                self.board[row+1][col]='.'
                if col!=0:
                    self.board[row+1][col-1]='.'
                if col!=9:
                    self.board[row+1][col+1]='.'
            if row!=0:
                self.board[row-1][col]='.'
                if col!=0:
                    self.board[row-1][col-1]='.'
                if col!=9:
                    self.board[row-1][col+1]='.'
            if col!=0:
                self.board[row][col-1]='.'

        if value=='r':
            if row!=9:
                self.board[row+1][col]='.'
                if col!=9:
                    self.board[row+1][col+1]='.'
                if col!=0:
                    self.board[row+1][col-1]='.'
            if row!=0:
                self.board[row-1][col]='.'
                if col!=9:
                    self.board[row-1][col+1]='.'
                if col!=0:
                    self.board[row-1][col-1]='.'
            if col!=9:
                self.board[row][col+1]='.' 
             
        if value=='t':
            if col!=9:
                self.board[row][col+1]='.'
                if row!=0:
                    self.board[row-1][col+1]='.'
                if row!=9:
                    self.board[row+1][col+1]='.'
            if col!=0:
                self.board[row][col-1]='.'
                if row!=0:
                    self.board[row-1][col-1]='.'
                if row!=9:
                    self.board[row+1][col-1]='.'
            if row!=0:
                self.board[row-1][col]='.'

        if value=='b':
            if col!=9:
                self.board[row][col+1]='.'
                if row!=9:
                    self.board[row+1][col+1]='.'
                if row!=0:
                    self.board[row-1][col+1]='.'
            
            if col!=0:
                self.board[row][col-1]='.'
                if row!=9:
                    self.board[row+1][col-1]='.'
                if row !=0:
                    self.board[row-1][col-1]='.'
            if row!=9:
                self.board[row+1][col]='.'

        if value=='m':
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'

    def checkFullShips(self):
        for ship in self.hintedShips:
            # verificar na horizontal
            if self.board[ship[0]][ship[1]] == 'l':
                if (self.board[ship[0]][ship[1]+1]=='r'):
                    #adciona um barco 1x2 horizontal
                    self.shipsLeft[1]-=1
                    self.row_counts[ship[0]]-=2
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.hintedShips.remove(ship)
                    self.hintedShips.remove((ship[0],ship[1]+1))
                    continue

                elif(self.board[ship[0]][ship[1]+1]=='m') and self.board[ship[0]][ship[1]+2]=='r':
                    #adciona um barco 1x3 horizontal
                    self.shipsLeft[2]-=1
                    self.row_counts[ship[0]]-=3
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.col_counts[ship[1]+2]-=1
                    self.hintedShips.remove(ship)
                    self.hintedShips.remove((ship[0],ship[1]+1))
                    self.hintedShips.remove((ship[0],ship[1]+2))
                    continue

                elif(self.board[ship[0]][ship[1]+1]=='m') and self.board[ship[0]][ship[1]+2]=='m' and self.board[ship[0]][ship[1]+3]=='r':
                    #adciona um barco 1x4 horizontal
                    
                    self.shipsLeft[3]-=1
                    self.row_counts[ship[0]]-=4
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.col_counts[ship[1]+2]-=1
                    self.col_counts[ship[1]+3]-=1
                    self.hintedShips.remove(ship)
                    self.hintedShips.remove((ship[0],ship[1]+1))
                    self.hintedShips.remove((ship[0],ship[1]+2))
                    self.hintedShips.remove((ship[0],ship[1]+3))
                    continue
                    
            # verificar na vertical         
            if self.board[ship[0]][ship[1]] == 't':
                if (self.board[ship[0]+1][ship[1]]=='b'):
                    #adciona um barco 1x2 vert
                    
                    self.shipsLeft[1]-=1
                    self.col_counts[ship[1]]-=2
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]+1]-=1
                    self.hintedShips.remove(ship)
                    self.hintedShips.remove((ship[0]+1,ship[1]))
                    continue
                    
                elif(self.board[ship[0]+1][ship[1]]=='m') and self.board[ship[0]+2][ship[1]]=='b':
                    #adciona um barco 1x3 vert
                    
                    self.shipsLeft[2]-=1
                    self.col_counts[ship[1]]-=3
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]+1]-=1
                    self.row_counts[ship[0]+2]-=1
                    self.hintedShips.remove(ship)
                    self.hintedShips.remove((ship[0]+1,ship[1]))
                    self.hintedShips.remove((ship[0]+2,ship[1]))
                    continue
                    
                elif(self.board[ship[0]+1][ship[1]]=='m') and self.board[ship[0]+2][ship[1]]=='m' and self.board[ship[0]+3][ship[1]]=='b':
                    #adciona um barco 1x4 vert
                    
                    self.shipsLeft[3]-=1
                    self.col_counts[ship[1]]-=4
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]+1]-=1
                    self.row_counts[ship[0]+2]-=1
                    self.row_counts[ship[0]+3]-=1
                    self.hintedShips.remove(ship)
                    self.hintedShips.remove((ship[0]+1,ship[1]))
                    self.hintedShips.remove((ship[0]+2,ship[1]))
                    self.hintedShips.remove((ship[0]+3,ship[1]))
                    continue

    def shipCompleteInference(self):
        for ship in self.hintedShips:
            #verificar se ta nas bordas, se não tiver percorrer a procura de uma agua, ou de um right ou de um middle para inferirmos mais
            if self.board[ship[0]][ship[1]] =='l':
                #se estiver na penultima coluna
                if ship[1]==8:
                    if self.board[ship[0]][ship[1]+1]=='r':
                        self.hintedShips.remove((ship[0],ship[1]+1))
                    self.board[ship[0]][ship[1]+1]='r'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[8]-=1
                    self.col_counts[9]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se tiver uma agua 2 coordenadas a direita então é um barco de 2
                if ship[1]<8 and (self.board[ship[0]][ship[1]+2]=='w' or self.board[ship[0]][ship[1]+2]=='.'):
                    print('a')
                    if self.board[ship[0]][ship[1]+1]=='r':
                        self.hintedShips.remove((ship[0],ship[1]+1))
                    self.board[ship[0]][ship[1]+1]='r'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se não houver barcos de 2 e tiver uma agua 3 coordenadas a direita então é um barco de 3
                elif ship[1]<7 and self.shipsLeft[1]==0 and (self.board[ship[0]][ship[1]+3]=='w' or self.board[ship[0]][ship[1]+3]=='.'):
                    print('b')
                    if self.board[ship[0]][ship[1]+2]=='r':
                        self.hintedShips.remove((ship[0],ship[1]+2))
                    self.board[ship[0]][ship[1]+2]='r'
                    if self.board[ship[0]][ship[1]+1]=='m':
                        self.hintedShips.remove((ship[0],ship[1]+1))
                    self.board[ship[0]][ship[1]+1]='m'
                    self.row_counts[ship[0]]-=3
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.col_counts[ship[1]+2]-=1
                    self.shipsLeft[2]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se não houver barcos de 2 nem 3 e tiver uma agua 4 coordenadas a direita então é um barco de 4
                elif ship[1]<6 and self.shipsLeft[1]==0 and self.shipsLeft[2]==0 and (self.board[ship[0]][ship[1]+4]=='w' or self.board[ship[0]][ship[1]+4]=='.'):
                    print('c')
                    if self.board[ship[0]][ship[1]+3]=='r':
                        self.hintedShips.remove((ship[0],ship[1]+3))
                    self.board[ship[0]][ship[1]+3]='r'
                    if self.board[ship[0]][ship[1]+2]=='m':
                        self.hintedShips.remove((ship[0],ship[1]+2))
                    self.board[ship[0]][ship[1]+2]='m'
                    if self.board[ship[0]][ship[1]+1]=='m':
                        self.hintedShips.remove((ship[0],ship[1]+1))
                    self.board[ship[0]][ship[1]+1]='m'
                    self.row_counts[ship[0]]-=4
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.col_counts[ship[1]+2]-=1
                    self.col_counts[ship[1]+3]-=1
                    self.shipsLeft[3]-=1
                    self.hintedShips.remove(ship)
                    continue

                #se tiver algum right no range de 2-3 então preenche o middle e cria o barco
                for i in range(2,min(4,10-ship[1])):
                    if self.board[ship[0]][ship[1]+i]=='r':
                        print('d')
                        self.hintedShips.remove((ship[0],ship[1]+i))
                        if (i==2):
                            if self.board[ship[0]][ship[1]+1]=='m':
                                self.hintedShips.remove((ship[0],ship[1]+1))
                            self.board[ship[0]][ship[1]+1]='m'
                            self.shipsLeft[2]-=1
                            self.row_counts[ship[0]]-=3
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]+1]-=1
                            self.col_counts[ship[1]+2]-=1
                            self.hintedShips.remove(ship)
                            break
                        if (i==3):
                            if self.board[ship[0]][ship[1]+1]=='m':
                                self.hintedShips.remove((ship[0],ship[1]+1))
                            self.board[ship[0]][ship[1]+1]='m'
                            if self.board[ship[0]][ship[1]+1]=='m':
                                self.hintedShips.remove((ship[0],ship[1]+2))
                            self.board[ship[0]][ship[1]+2]='m'
                            self.shipsLeft[3]-=1
                            self.row_counts[ship[0]]-=4
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]+1]-=1
                            self.col_counts[ship[1]+2]-=1
                            self.col_counts[ship[1]+3]-=1
                            self.hintedShips.remove(ship)
                            break
                continue

            if self.board[ship[0]][ship[1]]=='r':
                #se estiver na penultima coluna
                if ship[1]==1:
                    if self.board[ship[0]][ship[1]-1]=='l':
                        self.hintedShips.remove((ship[0],ship[1]-1))
                    self.board[ship[0]][ship[1]-1]='l'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[0]-=1
                    self.col_counts[1]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se tiver uma agua 2 coordenadas a direita então é um barco de 2
                if ship[1]>1 and (self.board[ship[0]][ship[1]-2]=='w' or self.board[ship[0]][ship[1]-2]=='.'):
                    if self.board[ship[0]][ship[1]-1]=='l':
                        self.hintedShips.remove((ship[0],ship[1]-1))
                    self.board[ship[0]][ship[1]-1]='l'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]-1]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se não houver barcos de 2 e tiver uma agua 3 coordenadas a direita então é um barco de 3
                elif ship[1]>2 and self.shipsLeft[1]==0 and (self.board[ship[0]][ship[1]-3]=='w' or self.board[ship[0]][ship[1]-3]=='.'):
                    if self.board[ship[0]][ship[1]-2]=='l':
                        self.hintedShips.remove((ship[0],ship[1]-2))
                    self.board[ship[0]][ship[1]-2]='l'

                    if self.board[ship[0]][ship[1]-1]=='m':
                        self.hintedShips.remove((ship[0],ship[1]-1))
                    self.board[ship[0]][ship[1]-1]='m'
                    self.row_counts[ship[0]]-=3
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]-1]-=1
                    self.col_counts[ship[1]-2]-=1
                    self.shipsLeft[2]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se não houver barcos de 2 nem 3 e tiver uma agua 4 coordenadas a direita então é um barco de 4
                elif ship[1]>3 and self.shipsLeft[1]==0 and self.shipsLeft[2]==0 and (self.board[ship[0]][ship[1]-4]=='w' or self.board[ship[0]][ship[1]-4]=='.'):
                    if self.board[ship[0]][ship[1]-3]=='l':
                        self.hintedShips.remove((ship[0],ship[1]-3))
                    self.board[ship[0]][ship[1]-3]='l'
                    if self.board[ship[0]][ship[1]-2]=='m':
                        self.hintedShips.remove((ship[0],ship[1]-2))
                    self.board[ship[0]][ship[1]-2]='m'
                    if self.board[ship[0]][ship[1]-1]=='m':
                        self.hintedShips.remove((ship[0],ship[1]-1))
                    self.board[ship[0]][ship[1]-1]='m'
                    self.row_counts[ship[0]]-=4
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]-1]-=1
                    self.col_counts[ship[1]-2]-=1
                    self.col_counts[ship[1]-3]-=1
                    self.shipsLeft[3]-=1
                    self.hintedShips.remove(ship)
                    continue

                #se tiver algum right no range de 2-3 então preenche o middle e cria o barco
                #TODO
                for i in range(2,min(4,ship[1])):
                    if self.board[ship[0]][ship[1]-i]=='l':
                        self.hintedShips.remove((ship[0],ship[1]-i))
                        if (i==2):
                            if self.board[ship[0]][ship[1]-1]=='m':
                                self.hintedShips.remove((ship[0],ship[1]-1))
                            self.board[ship[0]][ship[1]-1]='m'
                            self.shipsLeft[2]-=1
                            self.row_counts[ship[0]]-=3
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]-1]-=1
                            self.col_counts[ship[1]-2]-=1
                            self.hintedShips.remove(ship)
                            break
                        if (i==3):
                            if self.board[ship[0]][ship[1]-1]=='m':
                                self.hintedShips.remove((ship[0],ship[1]-1))
                            self.board[ship[0]][ship[1]-1]='m'
                            if self.board[ship[0]][ship[1]-2]=='m':
                                self.hintedShips.remove((ship[0],ship[1]-2))
                            self.board[ship[0]][ship[1]-2]='m'
                            self.shipsLeft[3]-=1
                            self.row_counts[ship[0]]-=4
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]-1]-=1
                            self.col_counts[ship[1]-2]-=1
                            self.col_counts[ship[1]-3]-=1
                            self.hintedShips.remove(ship)
                            break
                continue

            if self.board[ship[0]][ship[1]]=='t':
                #se estiver na penultima coluna
                if ship[0]==8:
                    if self.board[ship[0]+1][ship[1]]=='b':
                        self.hintedShips.remove((ship[0]+1,ship[1]))
                    self.board[ship[0]+1][ship[1]]='b'
                    self.col_counts[ship[1]]-=2
                    self.row_counts[8]-=1
                    self.row_counts[9]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue

                if ship[0]<8 and (self.board[ship[0]+2][ship[1]]=='w' or self.board[ship[0]+2][ship[1]]=='.'):
                    if self.board[ship[0]+1][ship[1]]=='b':
                        self.hintedShips.remove((ship[0]+1,ship[1]))
                    self.board[ship[0]+1][ship[1]]='b'
                    self.col_counts[ship[1]]-=2
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]+1]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se não houver barcos de 2 e tiver uma agua 3 coordenadas a direita então é um barco de 3
                elif ship[0]<7 and self.shipsLeft[1]==0 and (self.board[ship[0]+3][ship[1]]=='w' or self.board[ship[0]+3][ship[1]]=='.'):
                    if self.board[ship[0]+2][ship[1]]=='b':
                        self.hintedShips.remove((ship[0]+2,ship[1]))
                    self.board[ship[0]+2][ship[1]]='b'
                    if self.board[ship[0]+1][ship[1]]=='m':
                        self.hintedShips.remove((ship[0]+1,ship[1]))
                    self.board[ship[0]+1][ship[1]]='m'
                    self.col_counts[ship[1]]-=3
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]+1]-=1
                    self.row_counts[ship[0]+2]-=1
                    self.shipsLeft[2]-=1
                    self.hintedShips.remove(ship)
                    continue

                elif ship[0]<6 and self.shipsLeft[1]==0 and self.shipsLeft[2]==0 and (self.board[ship[0]+4][ship[1]]=='w' or self.board[ship[0]+4][ship[1]]=='.'):
                    if self.board[ship[0]+3][ship[1]]=='b':
                        self.hintedShips.remove((ship[0]+3,ship[1]))
                    self.board[ship[0]+3][ship[1]]='b'
                    if self.board[ship[0]+2][ship[1]]=='m':
                        self.hintedShips.remove((ship[0]+2,ship[1]))
                    self.board[ship[0]+2][ship[1]]='m'
                    if self.board[ship[0]+1][ship[1]]=='m':
                        self.hintedShips.remove((ship[0]+1,ship[1]))
                    self.board[ship[0]+1][ship[1]]='m'
                    self.col_counts[ship[1]]-=4
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]+1]-=1
                    self.row_counts[ship[0]+2]-=1
                    self.row_counts[ship[0]+3]-=1
                    self.shipsLeft[3]-=1
                    self.hintedShips.remove(ship)
                    continue

                #se tiver algum right no range de 2-3 então preenche o middle e cria o barco
                for i in range(2,min(4,10-ship[0])):
                    if self.board[ship[0]+i][ship[1]]=='b':
                        self.hintedShips.remove((ship[0]+i,ship[1]))
                        if (i==2):
                            if self.board[ship[0]+1][ship[1]]=='m':
                                self.hintedShips.remove((ship[0]+1,ship[1]))
                            self.board[ship[0]+1][ship[1]]='m'
                            self.shipsLeft[2]-=1
                            self.col_counts[ship[1]]-=3
                            self.row_counts[ship[0]]-=1
                            self.row_counts[ship[0]+1]-=1
                            self.row_counts[ship[0]+2]-=1
                            self.hintedShips.remove(ship)
                            break
                        if (i==3):
                            if self.board[ship[0]+1][ship[1]]=='m':
                                self.hintedShips.remove((ship[0]+1,ship[1]))
                            self.board[ship[0]+1][ship[1]]='m'
                            if self.board[ship[0]+2][ship[1]]=='m':
                                self.hintedShips.remove((ship[0]+2,ship[1]))
                            self.board[ship[0]+2][ship[1]]='m'
                            self.shipsLeft[3]-=1
                            self.col_counts[ship[1]]-=4
                            self.row_counts[ship[0]]-=1
                            self.row_counts[ship[0]+1]-=1
                            self.row_counts[ship[0]+2]-=1
                            self.row_counts[ship[0]+3]-=1
                            self.hintedShips.remove(ship)
                            break
                
                continue

            if self.board[ship[0]][ship[1]]=='b':
                #se estiver na penultima coluna
                if ship[0]==1:
                    if self.board[ship[0]-1][ship[1]]=='t':
                        self.hintedShips.remove((ship[0]-1,ship[1]))
                    self.board[ship[0]-1][ship[1]]='t'
                    self.col_counts[ship[1]]-=2
                    self.row_counts[0]-=1
                    self.row_counts[1]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue

                if ship[0]>1 and (self.board[ship[0]-2][ship[1]]=='w' or self.board[ship[0]-2][ship[1]]=='.'):
                    if self.board[ship[0]-1][ship[1]]=='t':
                        self.hintedShips.remove((ship[0]-1,ship[1]))
                    self.board[ship[0]-1][ship[1]]='t'
                    self.col_counts[ship[1]]-=2
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]-1]-=1
                    self.shipsLeft[1]-=1
                    self.hintedShips.remove(ship)
                    continue
                
                #se não houver barcos de 2 e tiver uma agua 3 coordenadas a direita então é um barco de 3
                elif ship[0]>2 and self.shipsLeft[1]==0 and (self.board[ship[0]-3][ship[1]]=='w' or self.board[ship[0]-3][ship[1]]=='.'):
                    if self.board[ship[0]-2][ship[1]]=='t':
                        self.hintedShips.remove((ship[0]-2,ship[1]))
                    self.board[ship[0]-2][ship[1]]='t'
                    if self.board[ship[0]-1][ship[1]]=='m':
                        self.hintedShips.remove((ship[0]-1,ship[1]))
                    self.board[ship[0]-1][ship[1]]='m'
                    self.col_counts[ship[1]]-=3
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]-1]-=1
                    self.row_counts[ship[0]-2]-=1
                    self.shipsLeft[2]-=1
                    self.hintedShips.remove(ship)
                    continue

                elif ship[0]>3 and self.shipsLeft[1]==0 and self.shipsLeft[2]==0 and (self.board[ship[0]-4][ship[1]]=='w' or self.board[ship[0]-4][ship[1]]=='.'):
                    if self.board[ship[0]-3][ship[1]]=='t':
                        self.hintedShips.remove((ship[0]-3,ship[1]))
                    self.board[ship[0]-3][ship[1]]='t'
                    if self.board[ship[0]-2][ship[1]]=='m':
                        self.hintedShips.remove((ship[0]-2,ship[1]))
                    self.board[ship[0]-2][ship[1]]='m'
                    if self.board[ship[0]-1][ship[1]]=='m':
                        self.hintedShips.remove((ship[0]-1,ship[1]))
                    self.board[ship[0]-1][ship[1]]='m'
                    self.col_counts[ship[1]]-=4
                    self.row_counts[ship[0]]-=1
                    self.row_counts[ship[0]-1]-=1
                    self.row_counts[ship[0]-2]-=1
                    self.row_counts[ship[0]-3]-=1
                    self.shipsLeft[3]-=1
                    self.hintedShips.remove(ship)
                    continue

                #se tiver algum right no range de 2-3 então preenche o middle e cria o barco
                for i in range(2,min(4,ship[0])):
                    if self.board[ship[0]-i][ship[1]]=='t':
                        self.hintedShips.remove((ship[0]-i,ship[1]))
                        if (i==2):
                            if self.board[ship[0]-1][ship[1]]=='m':
                                self.hintedShips.remove((ship[0]-1,ship[1]))
                            self.board[ship[0]-1][ship[1]]='m'
                            self.shipsLeft[2]-=1
                            self.col_counts[ship[1]]-=3
                            self.row_counts[ship[0]]-=1
                            self.row_counts[ship[0]-1]-=1
                            self.row_counts[ship[0]-2]-=1
                            self.hintedShips.remove(ship)
                            break
                        if (i==3):
                            if self.board[ship[0]-1][ship[1]]=='m':
                                self.hintedShips.remove((ship[0]-1,ship[1]))
                            self.board[ship[0]-1][ship[1]]='m'
                            if self.board[ship[0]-2][ship[1]]=='m':
                                self.hintedShips.remove((ship[0]-2,ship[1]))
                            self.board[ship[0]-2][ship[1]]='m'
                            self.shipsLeft[3]-=1
                            self.col_counts[ship[1]]-=4
                            self.row_counts[ship[0]]-=1
                            self.row_counts[ship[0]-1]-=1
                            self.row_counts[ship[0]-2]-=1
                            self.row_counts[ship[0]-3]-=1
                            self.hintedShips.remove(ship)
                            break

    def inferences(self):
        #Infere colunas ou linhas a 0
        for i in range(10):
            if self.row_counts[i]==0:
                for j in range(10):
                    if self.board[i][j]=='0':
                        self.board[i][j]="."

            if self.col_counts[i]==0:
                for j in range(10):
                    if self.board[i][j]=='0':
                        self.board[j][i]="."
        #Verifica 1x2 que estao presos à parede
            if self.board[i][8]=="l":
                self.board[i][9]="r"
                #meter aguas
                self.updateSurroundOfAction((i,8,"l",2))
                #tirar das counts
                self.row_counts[i]-=2
                self.col_counts[8]-=1
                self.col_counts[9]-=1
                self.hintedShips.remove((i,8))
                self.shipsLeft[1]-=1

            if self.board[i][1]=="r":
                self.board[i][0]="l"
                #meterAguas
                self.updateSurroundOfAction((i,0,"l",2))
                #tirar das counts
                self.row_counts[i]-=2
                self.col_counts[0]-=1
                self.col_counts[1]-=1
                self.hintedShips.remove((i,1))
                self.shipsLeft[1]-=1

            if self.board[1][i]=="b":
                
                self.board[0][i]="t"
                #meterAguas
                self.updateSurroundOfAction((0,i,"t",2))
                #tirar das counts
                self.col_counts[i]-=2
                self.row_counts[0]-=1
                self.row_counts[1]-=1
                self.hintedShips.remove((1,i))
                self.shipsLeft[1]-=1
            if self.board[8][i]=="t":
                #meterAguas
                self.board[9][i]="b"
                self.updateSurroundOfAction((8,i,"t",2))
                #tirar das counts
                self.col_counts[i]-=2
                self.row_counts[8]-=1
                self.row_counts[9]-=1
                self.hintedShips.remove((8,i))
                self.shipsLeft[1]-=1

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        # Lê a primeira linha
        row_counts = list(map(int, stdin.readline().split()[1:]))
        # Lê a segunda linha
        col_counts = list(map(int, stdin.readline().split()[1:]))
        board = Board(row_counts,col_counts)
        # Lê a terceira linha
        num_hints = int(stdin.readline().strip())
        # Lê as dicas e preenche o tabuleiro
        for i in range(num_hints):
            hint = stdin.readline().split()
            row, col = int(hint[1]), int(hint[2])
            value = hint[3].lower()
            board.initialHints.append((row,col,value.upper()))
            if value!='w' and value!='c':
                ship = (row,col)
                board.hintedShips.append(ship)
            if value=='c':
                board.shipsLeft[0]-=1
                board.row_counts[row]-=1
                board.col_counts[col]-=1
            board.board[row][col] = value
            if value!='w':
                board.updateSurroundOfCell((row,col,value))
        return board
    
    def get_inferences(self):
        self.ColumnsAndLinesDoneInference()
        
    def print_board(self) -> None:
        for i in range(10):
            for j in range(10):
                print(self.board[i][j],end='')
            print()

    def print_board_with_hints(self) -> None:
        for i in range(10):
            print(self.col_counts[i], end='')
        print()
        for i in range(10):
            for j in range(10):
                print(self.board[i][j],end='')
            print(' ',end='')
            print(self.row_counts[i])


    # mete agua nas linhas e colunas que ja estao feitas.
    def ColumnsAndLinesDoneInference(self):
        for i in range(10):
            if self.row_counts[i]==0:
                for k in range (10):
                    if self.board[i][k]=='0':
                        self.board[i][k]="."
            if self.col_counts[i]==0:
                for k in range (10):
                    if self.board[k][i]=='0':
                        self.board[k][i]="."

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = board
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        #(x,y,('l' or 't'),size)
        actions = []

        if not state.board.noHintedShips():
        #parte das hinted ships incompletas
            for ship in state.board.hintedShips:
                if state.board.board[ship[0]][ship[1]] == "l":
                    #este array representa todas as maneiras de completar a hint
                    #pode ser um de 2 ?
                    if(ship[1]<9 and state.board.row_counts[ship[0]]>=2 and state.board.board[ship[0]][ship[1]+1] == "0"):
                        #sim,epode ser um de 3?
                        if(ship[1]<8 and state.board.row_counts[ship[0]]>=3 and state.board.board[ship[0]][ship[1]+1] == "0" and state.board.board[ship[0]][ship[1]+2] == "0"):
                            #sim, pode ser um de 4 ?
                            if(ship[1]<7 and state.board.row_counts[ship[0]]>=4 and state.board.board[ship[0]][ship[1]+1] == "0" and state.board.board[ship[0]][ship[1]+2] == "0" and state.board.board[ship[0]][ship[1]+3] == "0"):
                                #sim
                                #Adciona uma acao 1x4
                                actions.append((ship[0],ship[1],"l",4))
                            #Adciona uma acao 1x3
                            actions.append((ship[0],ship[1],"l",3))
                        #Adciona uma acao 1x2
                        actions.append((ship[0],ship[1],"l",2))
                    #adciona ao array de acoes totais
                    state.board.hintedShips.remove(ship)
                    break
                    
                elif state.board.board[ship[0]][ship[1]] == "r":
                    #este array representa todas as maneiras de completar a hint
                    #pode ser um de 2 ?
                    if(ship[1]>0 and state.board.row_counts[ship[0]]>=2 and state.board.board[ship[0]][ship[1]-1] == "0"):
                        #sim,epode ser um de 3?
                        if(ship[1]>1 and state.board.row_counts[ship[0]]>=3 and state.board.board[ship[0]][ship[1]-1] == "0" and state.board.board[ship[0]][ship[1]-2] == "0"):
                            #sim, pode ser um de 4 ?
                            if(ship[1]>2 and state.board.row_counts[ship[0]]>=4 and state.board.board[ship[0]][ship[1]-1] == "0" and state.board.board[ship[0]][ship[1]-2] == "0" and state.board.board[ship[0]][ship[1]-3] == "0"):
                                #sim
                                #Adciona uma acao 1x4
                                actions.append((ship[0],ship[1]-3,"l",4))
                            #Adciona uma acao 1x3
                            actions.append((ship[0],ship[1]-2,"l",3))
                        #Adciona uma acao 1x2
                        actions.append((ship[0],ship[1]-1,"l",2))
                    #adciona ao array de acoes totais
                    state.board.hintedShips.remove(ship)
                    break
                
                elif state.board.board[ship[0]][ship[1]] == "t":
                    #este array representa todas as maneiras de completar a hint
                    #pode ser um de 2 ?
                    if(ship[0]<9 and state.board.col_counts[ship[1]]>=2 and state.board.board[ship[0]+1][ship[1]] == "0"):
                        #sim,epode ser um de 3?
                        if(ship[0]<8 and state.board.col_counts[ship[1]]>=3 and state.board.board[ship[0]+1][ship[1]] == "0" and state.board.board[ship[0]+2][ship[1]] == "0"):
                            #sim, pode ser um de 4 ?
                            if(ship[0]<7 and state.board.col_counts[ship[1]]>=4 and state.board.board[ship[0]+1][ship[1]] == "0" and state.board.board[ship[0]+2][ship[1]] == "0" and state.board.board[ship[0]+3][ship[1]] == "0"):
                                #sim
                                #Adciona uma acao 1x4
                                actions.append((ship[0],ship[1],"t",4))
                            #Adciona uma acao 1x3
                            actions.append((ship[0],ship[1],"t",3))
                        #Adciona uma acao 1x2
                        actions.append((ship[0],ship[1],"t",2))
                    #adciona ao array de acoes totais
                    state.board.hintedShips.remove(ship)
                    break

                elif state.board.board[ship[0]][ship[1]] == "b":
                    #este array representa todas as maneiras de completar a hint
                    #pode ser um de 2 ?
                    if(ship[0]>0 and state.board.col_counts[ship[1]]>=2 and state.board.board[ship[0]-1][ship[1]] == "0"):
                        #sim,epode ser um de 3?
                        if(ship[0]>1 and state.board.col_counts[ship[1]]>=3 and state.board.board[ship[0]-1][ship[1]] == "0" and state.board.board[ship[0]-2][ship[1]] == "0"):
                            #sim, pode ser um de 4 ?
                            if(ship[0]>2 and state.board.col_counts[ship[1]]>=4 and state.board.board[ship[0]-1][ship[1]] == "0" and state.board.board[ship[0]-2][ship[1]] == "0" and state.board.board[ship[0]-3][ship[1]] == "0"):
                                #sim
                                #Adciona uma acao 1x4
                                actions.append((ship[0]-3,ship[1],"t",4))
                            #Adciona uma acao 1x3
                            actions.append((ship[0]-2,ship[1],"t",3))
                        #Adciona uma acao 1x2
                        actions.append((ship[0]-1,ship[1],"t",2))
                    #adciona ao array de acoes totais
                    state.board.hintedShips.remove(ship)
                    break
                
                elif state.board.board[ship[0]][ship[1]]=="m":
                    #se for um barco na horizontal
                    if (ship[0]==9 or ship[0]==0 or state.board.board[ship[0]+1][ship[1]]=='w' or state.board.board[ship[0]+1][ship[1]]=='.' or state.board.board[ship[0]-1][ship[1]]=='w' or state.board.board[ship[0]-1][ship[1]]=='.'):
                        if state.board.row_counts[ship[0]]>=4:
                            if ship[1]+2<=9 and state.board.board[ship[0]][ship[1]+2]=='0':
                                actions.append((ship[0],ship[1]-1,'l',4))
                            if ship[1]-2>=0 and state.board.board[ship[0]][ship[1]-2]=='0':
                                actions.append((ship[0],ship[1]-2,'l',4))
                            
                        if state.board.row_counts[ship[0]]>=3 and (ship[1]+1<=9 or ship[1]-1>=0):
                            actions.append((ship[0],ship[1]-1,'l',3))
                    #barco na vertical
                    elif (ship[1]==9 or ship[1]==0 or state.board.board[ship[0]][ship[1]+1]=='w' or state.board.board[ship[0]][ship[1]+1]=='.' or state.board.board[ship[0]][ship[1]-1]=='w' or state.board.board[ship[0]][ship[1]-1]=='.'):
                        if state.board.col_counts[ship[1]]>=4:
                            if ship[0]+2<=9 and state.board.board[ship[0]+2][ship[1]]=='0':
                                actions.append((ship[0]-1,ship[1],'t',4))
                            if ship[0]-2>=0 and state.board.board[ship[0]-2][ship[1]]=='0':
                                actions.append((ship[0]-2,ship[1],'t',4))
                            
                        if state.board.col_counts[ship[1]]>=3 and (ship[0]+1<=9 or ship[0]-1>=0):
                            actions.append((ship[0]-1,ship[1],'t',3))

                    else:
                        if state.board.row_counts[ship[0]]>=4:
                            if ship[1]+2<=9 and state.board.board[ship[0]][ship[1]+2]=='0':
                                actions.append((ship[0],ship[1]-1,'l',4))
                            if ship[1]-2>=0 and state.board.board[ship[0]][ship[1]-2]=='0':
                                actions.append((ship[0],ship[1]-2,'l',4))

                        if state.board.row_counts[ship[0]]>=3 and (ship[1]+1<=9 or ship[1]-1>=0):
                            actions.append((ship[0],ship[1]-1,'l',3))

                        if state.board.col_counts[ship[1]]>=4:
                            if ship[0]+2<=9 and state.board.board[ship[0]+2][ship[1]]=='0':
                                actions.append((ship[0]-1,ship[1],'t',4))
                            if ship[0]-2>=0 and state.board.board[ship[0]-2][ship[1]]=='0':
                                actions.append((ship[0]-2,ship[1],'t',4))
                        
                        if state.board.col_counts[ship[1]]>=3 and (ship[0]+1<=9 or ship[0]-1>=0):
                            actions.append((ship[0]-1,ship[1],'t',3))

                    state.board.hintedShips.remove(ship)
                    break

        else :#barcos ao calhas
            for i in range(3,-1,-1):
                if state.board.shipsLeft[i]:
                    for j in range(10):
                        flag1=0
                        if state.board.row_counts[j]<i+1:
                            flag1=1
                        

                        if not flag1:
                            for k in range(10-i):
                                flag=0
                                if state.board.board[j][k]=='0' and state.board.col_counts[k]>0:
                                    for l in range(1,i+1):
                                        if state.board.board[j][k+l]!='0' or state.board.col_counts[k+l]==0:
                                            flag=1
                                            break

                                    #adicionar action
                                    if (flag):
                                        continue
                                    actions.append((j,k,'l',i+1))
                        
                        if (i==0):
                            continue

                        flag1=0
                        if state.board.col_counts[j]<i+1:
                            flag1=1

                        if not flag1:
                            for k in range(10-i):
                                flag=0
                                if state.board.board[k][j]=='0' and state.board.row_counts[k]>0:
                                    for l in range(1,i+1):
                                        if state.board.board[k+l][j]!='0' or state.board.row_counts[k+l]==0:
                                            flag=1
                                            break

                                    if (flag):
                                        continue
                                    actions.append((k,j,'t',i+1))
                            
                    break

        #random.shuffle(actions)
        return actions
    
    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        board = copy.deepcopy(state.board)

        #print('Action to make: ' + str(action))
        if (action[3]==4):
            if action[2]=='l':
                board.board[action[0]][action[1]] = 'l'
                board.board[action[0]][action[1]+1] = 'm'
                board.board[action[0]][action[1]+2] = 'm'
                board.board[action[0]][action[1]+3] = 'r'
                board.row_counts[action[0]]-=4
                for i in range(4):
                    board.col_counts[action[1]+i]-=1
            elif action[2]=='t':
                board.board[action[0]][action[1]]='t'
                board.board[action[0]+1][action[1]]='m'
                board.board[action[0]+2][action[1]]='m' 
                board.board[action[0]+3][action[1]]='b'
                board.col_counts[action[1]]-=4
                for i in range(4):
                    board.row_counts[action[0]+i]-=1
            board.shipsLeft[3]-=1

        elif (action[3]==3):
            if action[2]=='l':
                board.board[action[0]][action[1]] = 'l'
                board.board[action[0]][action[1]+1] = 'm'
                board.board[action[0]][action[1]+2] = 'r'
                board.row_counts[action[0]]-=3
                for i in range(3):
                    board.col_counts[action[1]+i]-=1
            elif action[2]=='t':
                board.board[action[0]][action[1]]='t'
                board.board[action[0]+1][action[1]]='m' 
                board.board[action[0]+2][action[1]]='b'
                board.col_counts[action[1]]-=3
                for i in range(3):
                    board.row_counts[action[0]+i]-=1
            board.shipsLeft[2]-=1

        elif (action[3]==2):
            if action[2]=='l':
                board.board[action[0]][action[1]] = 'l'
                board.board[action[0]][action[1]+1] = 'r'
                board.row_counts[action[0]]-=2
                for i in range(2):
                    board.col_counts[action[1]+i]-=1
            elif action[2]=='t':
                board.board[action[0]][action[1]]='t' 
                board.board[action[0]+1][action[1]]='b'
                board.col_counts[action[1]]-=2
                for i in range(2):
                    board.row_counts[action[0]+i]-=1

            board.shipsLeft[1]-=1
        
        elif (action[3]==1):
            board.board[action[0]][action[1]]='c'
            board.col_counts[action[1]]-=1
            board.row_counts[action[0]]-=1

            board.shipsLeft[0]-=1

        board.updateSurroundOfAction(action)
        board.ColumnsAndLinesDoneInference()

        return BimaruState(board)
    
    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.noShipsLeft() and state.board.hintsEmpty()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

if __name__ == "__main__":
    

    board = Board.parse_instance()
    board.shipCompleteInference()
    board.ColumnsAndLinesDoneInference()
    #board.inferences()
    #print(board.shipsLeft)
    problem = Bimaru(BimaruState(board))
    goal_node = depth_first_tree_search(problem)
    goal_node.state.board.updateInitialHints()
    goal_node.state.board.print_board()
