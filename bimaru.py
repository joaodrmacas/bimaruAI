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

class ShipCell:
    def __init__(self,row,col,type):
        self.coord = (row,col)
        self.type = type

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
        self.shipsPlaced = []
        self.shipsLeft = [4,3,2,1]

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row==9:
            return (None,self.board[row-1][col])
        elif row==0:
            return (self.board[row+1][col],None)
        return (self.board[row+1][col],self.board[row-1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
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
            value = hint[3]
            ship = ShipCell((row,col),value)
            board.shipsPlaced.append(ship)
            if value=='C':
                board.shipsLeft[0]-=1
            board.board[row][col] = value
        return board
    
    def get_inferences(self,arr):
        self.ColumnsAndLinesDoneInference()
        print(self.row_counts)
        print(self.col_counts)
        for coord in arr:
            self.surroundedShipInference(coord[0],coord[1])

    def print_board(self) -> None:
        for i in range(10):
            for j in range(10):
                print(self.board[i][j],end='')
            print()

    def surroundedShipInference(self,row:int,col:int):
        ship = self.get_value(row,col)
        min_coord = 0
        max_coord = 9
        if (ship=='0' or ship=='W' or ship=='.'):
            print('surroundedShipInference error: no ship was selected')
        
        if (ship=='C'):
            #Verticais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                if i != row:
                    if (self.board[i][col]!='W'):
                        self.board[i][col] = '.'    

            #Horizontais
            for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                if j != col:
                    if (self.board[row][j]!='W'):
                        self.board[row][j] = '.'

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='W'):
                            self.board[i][j] = '.'
        
        elif (ship=='T'):
            #Vertical
            if (row!=0):
                if (self.board[row-1][col]!='W'):
                    self.board[row-1][col] = '.'
            #Horizontais
            for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                if j != col:
                    if (self.board[row][j]!='W'):
                        self.board[row][j] = '.'

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='W'):
                            self.board[i][j] = '.'

        elif (ship=='M'):
            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='W'):
                            self.board[i][j] = '.'

        elif (ship=='B'):
            if (row!=9):
                if (self.board[row+1][col]!='W'):
                    self.board[row+1][col] = '.'
            #Horizontais
            for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                if j != col:
                    if (self.board[row][j]!='W'):
                        self.board[row][j] = '.'

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='W'):
                            self.board[i][j] = '.'
        
        elif (ship=='L'):
            if (col!=0):
                if (self.board[row][col-1]!='W'):
                    self.board[row][col-1]='.'
            #Verticais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                if i != row:
                    if (self.board[i][col]!='W'):
                        self.board[i][col] = '.'   

            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='W'):
                            self.board[i][j] = '.'

        elif (ship=='R'):
            if (col!=9):
                if (self.board[row][col+1]!='W'):
                    self.board[row][col+1]='.'

            #Verticais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                if i != row:
                    if (self.board[i][col]!='W'):
                        self.board[i][col] = '.'
            
            #Diagonais
            for i in range(max(row - 1, min_coord), min(row + 2, max_coord + 1)):
                for j in range(max(col - 1, min_coord), min(col + 2, max_coord + 1)):
                    if i != row and j != col and abs(row - i) == abs(col - j):
                        if (self.board[i][j]!='W'):
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

    
    def shipInference(self):
        for ship in self.shipsPlaced:
            # verificar 1x2
            if self.shipsLeft[2]:
                
                if ship.value == 'l':
                    if self.board[ship.coord[0]][ship.coord[1]+1]=='r':
                        self.shipsLeft[2]-=1
                        self.row_counts[ship.coord[0]]-=1 
                        
                    if self.board[ship.coord[0]+1][ship.coord[1]]!=:

            #verifcicar 1x3

    def spaceLeftHorizontalsInference(self):
        for i in range(10):
            
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
    a.get_inferences(a.shipsPlaced)
    a.print_board()
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
