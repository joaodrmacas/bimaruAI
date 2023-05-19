# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
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

class Ship:
    def __init__(self,type) -> None:
            
        self.type = type
        if (type==0):
            self.coords= [None for _ in range(4)]
        else:
            self.coords = [None for _ in range (type)]
        self.fullyplaced = False

    def isPlaced(self):
        return self.fullyplaced


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self,row_counts,col_counts,) -> None:
        self.board = [['0' for _ in range(10)] for _ in range(10)]
        self.row_counts = row_counts
        self.col_counts = col_counts
        self.hintedShips = []
        self.shipsLeft = [4,3,2,1]

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row==9:
            return (None,self.board[row-1][col])
        elif row==0:
            return (self.board[row+1][col],None)
        return (self.board[row+1][col],self.board[row-1][col])

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.board[row][col+1],self.board[row][col-1])

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
            if value!='w':
                ship = (row,col)
                board.hintedShips.append(ship)
            if value=='c':
                board.shipsLeft[0]-=1
            board.board[row][col] = value
        return board
    
    def get_inferences(self):
        self.ColumnsAndLinesDoneInference()
        print(self.row_counts)
        print(self.col_counts)
        for coord in self.hintedShips:
            self.surroundedShipInference(coord[0],coord[1])
        self.spaceLeftInference()
        print(self.shipsLeft)

    def print_board(self) -> None:
        for i in range(10):
            print(self.col_counts[i], end='')
        print()
        for i in range(10):
            for j in range(10):
                print(self.board[i][j],end='')
            print(' ',end='')
            print(self.row_counts[i])

    def surroundedShipInference(self,row:int,col:int):
        ship = self.get_value(row,col)
        min_coord = 0
        max_coord = 9
        if (ship=='0' or ship=='w' or ship=='.'):
            print('surroundedShipInference error: no ship was selected')
        
        if (ship=='c'):
            #Verticais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                if i != row:
                    if (self.board[i][col]!='w'):
                        self.board[i][col] = '.'    

            #Horizontais
            for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                if j != col:
                    if (self.board[row][j]!='w'):
                        self.board[row][j] = '.'

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'
        
        elif (ship=='t'):
            #Vertical
            if (row!=0):
                if (self.board[row-1][col]!='w'):
                    self.board[row-1][col] = '.'
            #Horizontais
            for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                if j != col:
                    if (self.board[row][j]!='w'):
                        self.board[row][j] = '.'

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'

        elif (ship=='m'):
            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'

        elif (ship=='b'):
            if (row!=9):
                if (self.board[row+1][col]!='w'):
                    self.board[row+1][col] = '.'
            #Horizontais
            for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                if j != col:
                    if (self.board[row][j]!='w'):
                        self.board[row][j] = '.'

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'
        
        elif (ship=='l'):
            if (col!=0):
                if (self.board[row][col-1]!='w'):
                    self.board[row][col-1]='.'
            #Verticais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                if i != row:
                    if (self.board[i][col]!='w'):
                        self.board[i][col] = '.'   

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'

        elif (ship=='r'):
            if (col!=9):
                if (self.board[row][col+1]!='w'):
                    self.board[row][col+1]='.'

            #Verticais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                if i != row:
                    if (self.board[i][col]!='w'):
                        self.board[i][col] = '.'
            
            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='w'):
                            self.board[i][j] = '.'
        else:
            print("surroundedShipInference error: unknown cell type")

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

    
    def shipInferenceInitial(self):
        for ship in self.hintedShips:
            # verificar na horizontal
            if self.board[ship[0]][ship[1]] == 'l':
                if (self.board[ship[0]][ship[1]+1]=='r') and ship[1] > 8 :
                    #adciona um barco 1x2 horizontal
                    if not self.shipsLeft[1]:
                        print("Erro ShipInferenceInitial a adicionar 1x2 horizontal")
                        exit()
                    self.shipsLeft[1]-=1
                    self.row_counts[ship[0]]-=2
                    if self.row_counts[ship[0]]<0:
                        print("Erro ShipInferenceInitial a adicionar 1x2 horizon")
                        exit()

                elif(self.board[ship[0]][ship[1]+1]=='m') and self.board[ship[0]+2][ship[1]]=='r'and ship[1] > 7:
                    #adciona um barco 1x3 horizontal
                    if not self.shipsLeft[2]:
                        print("Erro ShipInferenceInitial a adicionar 1x3 horizontal")
                        exit()
                    self.shipsLeft[2]-=1
                    self.row_counts[ship[0]]-=3
                    if self.row_counts[ship[0]]<0:
                        print("Erro ShipInferenceInitial a adicionar 1x3 horizontal")
                        exit()

                elif(self.board[ship[0]][ship[1]+1]=='m') and self.board[ship[0]+2][ship[1]]=='m' and self.board[ship[0]+3][ship[1]]=='r' and ship[1] > 6:
                    #adciona um barco 1x4 horizontal
                    if not self.shipsLeft[3]:
                        print("Erro ShipInferenceInitial a adcionar 1x4 horizontal")
                        exit()
                    self.shipsLeft[3]-=1
                    self.row_counts[ship[0]]-=4
                    if self.row_counts[ship[0]]<0:
                        print("Erro ShipInferenceInitial a adcionar 1x4 horizontal")
                        exit()
            
            # verificar na vertical         
            if self.board[ship[0]][ship[1]] == 't':
                if (self.board[ship[0]+1][ship[1]]=='b') and ship[0] > 8 :
                    #adciona um barco 1x2 vert
                    if not self.shipsLeft[1]:
                        print("Erro ShipInferenceInitial a adicionar 1x2 verti")
                        exit()
                    self.shipsLeft[1]-=1
                    self.col_counts[ship[1]]-=2
                    if self.col_counts[ship[1]]<0:
                        print("Erro ShipInferenceInitial a adicionar 1x2 verti")
                        exit()
                elif(self.board[ship[0]+1][ship[1]]=='m') and self.board[ship[0]+2][ship[1]]=='b'and ship[0] > 7:
                    #adciona um barco 1x3 vert
                    if not self.shipsLeft[2]:
                        print("Erro ShipInferenceInitial a adicionar 1x3 verti")
                        exit()
                    self.shipsLeft[2]-=1
                    self.col_counts[ship[1]]-=3
                    if self.col_counts[ship[1]]<0:
                        print("Erro ShipInferenceInitial a adicionar 1x3 verti")
                        exit()
                elif(self.board[ship[0]+1][ship[1]]=='m') and self.board[ship[0]+2][ship[1]]=='m' and self.board[ship[0]+3][ship[1]]=='b' and ship[0] > 6:
                    #adciona um barco 1x4 vert
                    if not self.shipsLeft[3]:
                        print("Erro ShipInferenceInitial a adicionar 1x4 verti")
                        exit()
                    self.shipsLeft[3]-=1
                    self.col_counts[ship[1]]-=4
                    if self.col_counts[ship[1]]<0:
                        print("Erro ShipInferenceInitial a adicionar 1x4 verti")
                        exit()
                    

    
    def shipCompleteInference(self):
        for ship in self.shipsLeft:
            #verificar se ta nas bordas, se não tiver percorrer a procura de uma agua, ou de um right ou de um middle para inferirmos mais
            if self.board[ship[0]][ship[1]]=='l':
                #se estiver na penultima coluna
                if ship[1]==8:
                    self.board[ship[0]][ship[1]+1]='r'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[8]-=1
                    self.col_counts[9]-=1
                    self.shipsLeft[1]-=1
                
                #se tiver uma agua 2 coordenadas a direita então é um barco de 2
                if ship[1]<8 and (self.board[ship[0]][ship[1]+2]=='w' or self.board[ship[0]][ship[1]+2]=='.'):
                    self.board[ship[0]][ship[1]+1]='r'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.shipsLeft[1]-=1
                
                #se não houver barcos de 2 e tiver uma agua 3 coordenadas a direita então é um barco de 3
                elif ship[1]<7 and self.shipsLeft[1]==0 and (self.board[ship[0]][ship[1]+3]=='w' or self.board[ship[0]][ship[1]+3]=='.'):
                    self.board[ship[0]][ship[1]+2]='r'
                    self.board[ship[0]][ship[1]+1]='m'
                    self.row_counts[ship[0]]-=3
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.col_counts[ship[1]+2]-=1
                    self.shipsLeft[2]-=1
                
                #se não houver barcos de 2 nem 3 e tiver uma agua 4 coordenadas a direita então é um barco de 4
                elif ship[1]<6 and self.shipsLeft[1]==0 and self.shipsLeft[2]==0 and (self.board[ship[0]][ship[1]+4]=='w' or self.board[ship[0]][ship[1]+4]=='.'):
                    self.board[ship[0]][ship[1]+3]='r'
                    self.board[ship[0]][ship[1]+2]='m'
                    self.board[ship[0]][ship[1]+1]='m'
                    self.row_counts[ship[0]]-=4
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]+1]-=1
                    self.col_counts[ship[1]+2]-=1
                    self.col_counts[ship[1]+3]-=1
                    self.shipsLeft[3]-=1

                #se tiver algum right no range de 2-3 então preenche o middle e cria o barco
                for i in range(2,min(4,10-ship[1])):
                    if self.board[ship[0],ship[1]+i]=='r':
                        if (i==2):
                            self.board[ship[0],ship[1]+1]='m'
                            self.shipsLeft[2]-=1
                            self.row_counts[ship[0]]-=3
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]+1]-=1
                            self.col_counts[ship[1]+2]-=1
                        if (i==3):
                            self.board[ship[0],ship[1]+1]='m'
                            self.board[ship[0],ship[1]+2]='m'
                            self.shipsLeft[3]-=1
                            self.row_counts[ship[0]]-=4
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]+1]-=1
                            self.col_counts[ship[1]+2]-=1
                            self.col_counts[ship[1]+3]-=1

            if self.board[ship[0]][ship[1]]=='r':
                #se estiver na penultima coluna
                if ship[1]==1:
                    self.board[ship[0]][ship[1]-1]='l'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[0]-=1
                    self.col_counts[1]-=1
                    self.shipsLeft[1]-=1
                
                #se tiver uma agua 2 coordenadas a direita então é um barco de 2
                if ship[1]>1 and (self.board[ship[0]][ship[1]-2]=='w' or self.board[ship[0]][ship[1]-2]=='.'):
                    self.board[ship[0]][ship[1]-1]='l'
                    self.row_counts[ship[0]]-=2
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]-1]-=1
                    self.shipsLeft[1]-=1
                
                #se não houver barcos de 2 e tiver uma agua 3 coordenadas a direita então é um barco de 3
                elif ship[1]>2 and self.shipsLeft[1]==0 and (self.board[ship[0]][ship[1]-3]=='w' or self.board[ship[0]][ship[1]-3]=='.'):
                    self.board[ship[0]][ship[1]-2]='l'
                    self.board[ship[0]][ship[1]-1]='m'
                    self.row_counts[ship[0]]-=3
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]-1]-=1
                    self.col_counts[ship[1]-2]-=1
                    self.shipsLeft[2]-=1
                
                #se não houver barcos de 2 nem 3 e tiver uma agua 4 coordenadas a direita então é um barco de 4
                elif ship[1]>3 and self.shipsLeft[1]==0 and self.shipsLeft[2]==0 and (self.board[ship[0]][ship[1]-4]=='w' or self.board[ship[0]][ship[1]-4]=='.'):
                    self.board[ship[0]][ship[1]-3]='l'
                    self.board[ship[0]][ship[1]-2]='m'
                    self.board[ship[0]][ship[1]-1]='m'
                    self.row_counts[ship[0]]-=4
                    self.col_counts[ship[1]]-=1
                    self.col_counts[ship[1]-1]-=1
                    self.col_counts[ship[1]-2]-=1
                    self.col_counts[ship[1]-3]-=1
                    self.shipsLeft[3]-=1

                #se tiver algum right no range de 2-3 então preenche o middle e cria o barco
                #TODO
                for i in range(2,min(4,ship[1])):
                    if self.board[ship[0],ship[1]-i]=='l':
                        if (i==2):
                            self.board[ship[0],ship[1]-1]='m'
                            self.shipsLeft[2]-=1
                            self.row_counts[ship[0]]-=3
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]-1]-=1
                            self.col_counts[ship[1]-2]-=1
                        if (i==3):
                            self.board[ship[0],ship[1]-1]='m'
                            self.board[ship[0],ship[1]-2]='m'
                            self.shipsLeft[3]-=1
                            self.row_counts[ship[0]]-=4
                            self.col_counts[ship[1]]-=1
                            self.col_counts[ship[1]-1]-=1
                            self.col_counts[ship[1]-2]-=1
                            self.col_counts[ship[1]-3]-=1

    
    def spaceLeftInference(self):
        for i in range(10):
            #deve dar para otimizar ao aproveitar o loop de dentro
            if (self.row_counts[i]!=0):
                coord = (0,0)
                inarow = 0
                emptycellscount = 0
                maxrow=0
                for j in range(10):
                    if self.board[i][j]=='0':
                        coord = (i,j)
                        inarow+=1
                        emptycellscount+=1
                    else:
                        if (inarow>maxrow):
                            maxrow=inarow
                        inarow=0
                if(inarow>maxrow):
                    maxrow=inarow

                if (maxrow==4 and self.shipsLeft[0]!=0):
                    continue
                
                if (maxrow==self.row_counts[i] and emptycellscount==self.row_counts[i]):
                    #adicionar barco
                    self.shipsLeft[maxrow-1]-=1 #retira o barco adicionado dos shipsLeft
                    self.row_counts[i]-=maxrow
                    if maxrow==1:
                        self.board[coord[0]][coord[1]] = 'c'
                        self.col_counts[coord[1]]-=1 #retirar das hints
                    else:
                        self.board[coord[0]][coord[1]]= 'r'
                        self.col_counts[coord[1]]-=1
                        for k in range(1,maxrow-1): #meter posicoes do middle
                            self.board[coord[0]][coord[1]-k]='m'
                            self.col_counts[coord[1]-k]-=1
                        self.board[coord[0]][coord[1]-maxrow-1]='l'
                        self.col_counts[coord[1]-maxrow-1]-=1
                elif (emptycellscount<=3 and emptycellscount==self.row_counts):
                    if (emptycellscount==2):
                        #TODO guardar as celulas com 0 para este loop? vale a pena
                        for k in range(10):
                            if (self.board[coord[0]][k]=='0'):
                                self.board[coord[0]][k]='c'
                                self.shipsLeft[0]-=1
                                self.row_counts[coord[0]]-=1
                                self.col_counts[k]-=1

                    elif (emptycellscount==3 and maxrow==1):
                        for k in range(10):
                            if self.board[coord[0]][k]=='0':
                                self.board[coord[0]][k]='c'
                                self.shipsLeft[0]-=1
                                self.row_counts[coord[0]]-=1
                                self.col_counts[k]-=1
                    
                    else:
                        for k in range(10):
                            if self.board[coord[0]][k]=='0':
                                if self.board[coord[0]][k+1]=='0': #pode dar index out of range? TODO
                                    self.board[coord[0]][k]='l'
                                    self.board[coord[0]][k+1]='r'
                                    self.shipsLeft[1]-=1
                                    self.row_counts[coord[0]]-=2
                                    self.col_counts[k]-=1
                                    self.col_counts[k+1]-=1
                                else:
                                    self.board[coord[0]][k]='c'
                                    self.shipsLeft[0]-=1
                                    self.row_counts[coord[0]]-=1
                                    self.col_counts[k]-=1

            if (self.col_counts[i]!=0):
                coord = (0,0)
                inarow = 0
                emptycellscount = 0
                maxrow=0
                for j in range(10):
                    if self.board[j][i]=='0':
                        coord = (j,i)
                        inarow+=1
                        emptycellscount+=1
                    else:
                        if (inarow>maxrow):
                            maxrow=inarow
                        inarow=0
                if (inarow>maxrow):
                    maxrow=inarow
                if (maxrow==4 and self.shipsLeft[0]!=0):
                    continue
                    
                if (maxrow==self.col_counts[i] and emptycellscount==self.row_counts[i]):
                    self.shipsLeft[maxrow-1]-=1
                    if (self.shipsLeft[maxrow-1]<0):
                        print('spaceLeftInference: error shipsLeft is negative')
                        exit()
                    self.col_counts[i]-=maxrow
                    if maxrow==1:
                        self.board[coord[0]][coord[1]]='c'
                        self.row_counts[coord[0]]-=1
                    else:
                        self.board[coord[0]][coord[1]]= 'r'
                        self.row_counts[coord[1]]-=1
                        for k in range(1,maxrow-1): #meter posicoes do middle
                            self.board[coord[0]-k][coord[1]]='m'
                            self.row_counts[coord[0]-k]-=1
                        self.board[coord[0]-maxrow-1][coord[1]]='l'
                        self.row_counts[coord[0]-maxrow-1]-=1
                

                elif (emptycellscount<=3 and emptycellscount==self.col_counts):
                    if (emptycellscount==2):
                        #TODO guardar as celulas com 0 para este loop? vale a pena
                        for k in range(10):
                            if (self.board[k][coord[1]]=='0'):
                                self.board[k][coord[1]]='c'
                                self.shipsLeft[0]-=1
                                if (self.shipsLeft[0]<0):
                                    print('spaceLeftInference: error shipsLeft is negative')
                                    exit()
                                self.col_counts[coord[1]]-=1
                                self.row_counts[k]-=1

                    elif (emptycellscount==3 and maxrow==1):
                        for k in range(10):
                            if self.board[k][coord[1]]=='0':
                                self.board[k][coord[1]]='c'
                                self.shipsLeft[0]-=1
                                if (self.shipsLeft[0]<0):
                                        print('spaceLeftInference: error shipsLeft is negative')
                                        exit()
                                self.col_counts[coord[1]]-=1
                                self.row_counts[k]-=1
                    
                    else:
                        for k in range(10):
                            if self.board[k][coord[1]]=='0':
                                if self.board[k+1][coord[1]]=='0': #pode dar index out of range? TODO
                                    self.board[k][coord[1]]='t'
                                    self.board[k+1][coord[1]]='b'
                                    self.shipsLeft[1]-=1
                                    if (self.shipsLeft[1]<0):
                                        print('spaceLeftInference: error shipsLeft is negative')
                                        exit()
                                    self.col_counts[coord[1]]-=2
                                    self.row_counts[k]-=1
                                    self.row_counts[k+1]-=1
                                else:
                                    self.board[k][coord[1]]='c'
                                    self.shipsLeft[0]-=1
                                    if (self.shipsLeft[0]<0):
                                        print('spaceLeftInference: error shipsLeft is negative')
                                        exit()
                                    self.row_counts[k]-=1
                                    self.col_counts[coord[1]]-=1

    # def shipInference(self):
    #     for ship in self.hintedShips:
            
    #         if self.get_value(ship[0],ship[1]) == 'L':
                

    # TODO: outros metodos da classe



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    a = Board.parse_instance()
    print(a.hintedShips)
    a.shipInferenceInitial()
    a.get_inferences()
    a.print_board()
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
