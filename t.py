# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 103369 Miguel o grande
# 000000 joao o pequeno

import sys
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

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self,row_counts,col_counts,) -> None:
        self.board = [['0' for _ in range(10)] for _ in range(10)]
        self.row_counts = row_counts
        self.col_counts = col_counts
        self.hintedShips = []
        self.shipsLeft = [4,3,2,1]

    def noHintedShips(self):
        return True if not self.hintedShips else False

    def noShipsLeft(self):
        for i in range(4):
            if self.shipsLeft[i] != 0:
                return False
        return True

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
            if value!='w' and value!='c':
                ship = (row,col)
                board.hintedShips.append(ship)
            if value=='c':
                board.shipsLeft[0]-=1
                board.row_counts[row]-=1
                board.col_counts[col]-=1
            board.board[row][col] = value
        return board
    
    def get_inferences(self):
        self.ColumnsAndLinesDoneInference()
        
    def print_board(self) -> None:
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
            #print('ShipsLeft',state.board.shipsLeft)
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
            # print('----------')
            # print('Resulted Board:')
            # board.print_board()
            # print('----------')
            # print('ShipsLeft: ' + str(board.shipsLeft))
            # print('HintedShips: '+ str(board.hintedShips))

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
            # print('----------')
            # print('Resulted Board:')
            # board.print_board()
            # print('----------')
            # print('ShipsLeft: ' + str(board.shipsLeft))
            # print('HintedShips: '+ str(board.hintedShips))

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
            # print('----------')
            # print('Resulted Board:')
            # board.print_board()
            # print('----------')
            # print('ShipsLeft: ' + str(board.shipsLeft))
            # print('HintedShips: '+ str(board.hintedShips))
        
        elif (action[3]==1):
            board.board[action[0]][action[1]]='c'
            board.col_counts[action[1]]-=1
            board.row_counts[action[0]]-=1

            board.shipsLeft[0]-=1
            # print('----------')
            # print('Resulted Board:')
            # board.print_board()
            # print('----------')
            # print('ShipsLeft: ' + str(board.shipsLeft))
            # print('HintedShips: '+ str(board.hintedShips))

        board.get_inferences()

        return BimaruState(board)
    
    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.noShipsLeft()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe



if __name__ == "__main__":
    
    board = Board.parse_instance()
    board.get_inferences()
    problem = Bimaru(BimaruState(board))
    goal_node = depth_first_tree_search(problem)
    goal_node.state.board.print_board()
