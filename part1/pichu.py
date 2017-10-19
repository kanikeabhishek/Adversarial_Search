#!/usr/bin/python2.7
import sys
import copy


"""
IDFS implementation
takes inital state
returns the best possible move
"""
white = ['P','R','Q','K','N','B'];
black = ['p','r','q','k','n','b'];

frontier = []

def printable_board(board):
    for i in board:
        print(i)
    print("--------------------------------------------------------------------------------------")

def isValidForParakeeth(board, row, col, i):
    if (row >= 0 and row <= 7 and col >= 0 and col <= 7):
        if i == 3:
            if board[row-1][col] == "." and board[row][col] == ".":
                return True
        elif i % 2 == 0 and board[row][col] in black:
            return True
        elif i == 1 and board[row][col] == ".":
            return True
    return False

def isValidorDisbale(board, row, col, row_list, col_list, i):
    if (row >= 0 and row <= 7 and col >= 0 and col <= 7):
        if board[row][col] == ".":
            return True
        row_list[i] *= 100; col_list[i] *= 100
        if board[row][col] in black:
            return True
        else:
            return False
    return False

def generatesuccessor(board):
    printable_board(board)
    for i in range(0,8):
        for j in range(0,8):
            '''
            if(board[i][j] == 'P'):
                move_parakeeth(board,i,j)
            if(board[i][j] == 'R'):
                move_robin(board,i,j)
            if(board[i][j] == 'B'):
                move_bluejay(board,i,j)
            if(board[i][j] == 'Q'):
                move_queztal(board,i,j)
            if(board[i][j] == 'K'):
                move_kingfisher(board,i,j)
            '''
            if(board[i][j] == 'N'):
                move_nighthawk(board,i,j)

def move_parakeeth(board,row,col):#not checking for quezals
    Parakeeth_Row = [1, 1, 1, 2]
    Parakeeth_Col = [-1, 0, 1, 0]

    for i in range(0, len(Parakeeth_Row)):
        row1 = row + Parakeeth_Row[i]
        col1 = col + Parakeeth_Col[i]
        if (isValidForParakeeth(board, row1, col1, i)):
            new_board = copy.deepcopy(board)
            new_board[row][col] = "."
            new_board[row1][col1] = "P"
            frontier.append(new_board)
            printable_board(frontier[-1])

def moveBird(board, row, col, possible_row, possible_col, possible_moves, iterations, bird):
    for i in range(possible_moves):
        for j in range(1, iterations):
            row1 = row + possible_row[i] * j
            col1 = col + possible_col[i] * j
            if (isValidorDisbale(board, row1, col1, possible_row, possible_col, i)):
                new_board = copy.deepcopy(board)
                new_board[row][col] = "."
                new_board[row1][col1] = bird
                frontier.append(new_board)
                printable_board(frontier[-1])

def move_queztal(board,row,col):
    Queztal_Row = [-1, -1, -1, 0, 1, 1, 1, 0]
    Queztal_Col = [-1, 0, 1, 1, 1, 0, -1, -1]
    moveBird(board, row, col, Queztal_Row, Queztal_Col, len(Queztal_Row), 8, 'Q')

def move_bluejay(board,row,col):
    BlueJay_Row = [-1, -1, 1, 1]
    BlueJay_Col = [-1, 1, 1, -1]
    moveBird(board, row, col, BlueJay_Row, BlueJay_Col, len(BlueJay_Row), 8, 'B')

def move_robin(board,row,col):
    Robin_Row = [0, -1, 0, 1]
    Robin_Col = [-1, 0, 1, 0]
    moveBird(board, row, col, Robin_Row, Robin_Col, len(Robin_Row), 8, 'R')

def move_kingfisher(board,row,col):
    KingFisher_Row = [1, 1, 1, 0, -1, -1, -1, 0]
    KingFisher_Col = [-1, 0, 1, 1, 1, 0, -1, -1]
    moveBird(board, row, col, KingFisher_Row, KingFisher_Col, len(KingFisher_Row), 2, 'K')

def move_nighthawk(board,row,col):
    NightHawk_Row = [1, 2, 2, 1, -1, -2, -2, -1]
    NightHawk_Col = [-2, -1, 1, 2, 2 ,1, -1, -2]
    moveBird(board, row, col, NightHawk_Row, NightHawk_Col, len(NightHawk_Row), 2, 'N')

def idfs(initial_board):
    generatesuccessor(initial_board)

def create_board(initial_state):
    board = list();
    for j in range(0,63,8):
        board.append(list(initial_state[j:j+8]))
    return board

def read_input():
    turn = sys.argv[1]
    initial_state = sys.argv[2]
    time = int(sys.argv[3])
    print(len(initial_state))
    return (turn,initial_state,time)

def main():
    (turn,initial_state,time) = read_input()
    #print(turn,initial_state,time)
    inital_board = create_board(initial_state)
    #print(inital_board)
    idfs(inital_board)



if __name__=="__main__":
    main()
