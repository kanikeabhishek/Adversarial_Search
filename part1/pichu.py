#!/usr/bin/python2.7
import sys
import copy


white = ['P','R','B','Q','K','N'];
black = ['p','r','b','q','k','n'];

me = []# not in use now can be removed or used later.
opposition = []

frontier = []
maxdepth = 2

def printable_board(board):
    for i in board:
        print(i)
    print("--------------------------------------------------------------------------------------")

def isValidForParakeeth(board, row, col, i):
    if (row >= 0 and row <= 7 and col >= 0 and col <= 7):
        if i == 3:
            if board[row-1][col] == "." and board[row][col] == ".":
                return True
        elif i % 2 == 0 and board[row][col] in opposition:
            return True
        elif i == 1 and board[row][col] == ".":
            return True
    return False

def isValidorDisbale(board, row, col, row_list, col_list, i):
    if (row >= 0 and row <= 7 and col >= 0 and col <= 7):
        if board[row][col] == ".":
            return True
        row_list[i] *= 100; col_list[i] *= 100
        #print(opposition)
        if board[row][col] in opposition:
            return True
        else:
            return False

def generatesuccessor(board,player):
    global frontier
    del frontier[:]
    identify_opponent(player)

    if player:
        (p,r,b,q,k,n) = white
    else:
        (p,r,b,q,k,n) = black

    for i in range(0,8):
        for j in range(0,8):
            if(board[i][j] == p):
                move_parakeeth(board,p,i,j)
            elif(board[i][j] == r):
                move_robin(board,r,i,j)
            elif(board[i][j] == b):
                move_bluejay(board,b,i,j)
            elif(board[i][j] == q):
                move_queztal(board,q,i,j)
            elif(board[i][j] == k):
                move_kingfisher(board,k,i,j)
            elif(board[i][j] == n):
                move_nighthawk(board,n,i,j)
    return frontier

def move_parakeeth(board,p,row,col):
    '''TBD:check for quezals and black pawn movements'''

    Parakeeth_Row = [1, 1, 1, 2]
    Parakeeth_Col = [-1, 0, 1, 0]

    for i in range(0, len(Parakeeth_Row)):
        row1 = row + Parakeeth_Row[i]
        col1 = col + Parakeeth_Col[i]
        if (isValidForParakeeth(board, row1, col1, i)):
            new_board = copy.deepcopy(board)
            new_board[row][col] = "."
            new_board[row1][col1] = p
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

def move_queztal(board,q,row,col):
    Queztal_Row = [-1, -1, -1, 0, 1, 1, 1, 0]
    Queztal_Col = [-1, 0, 1, 1, 1, 0, -1, -1]
    moveBird(board, row, col, Queztal_Row, Queztal_Col, len(Queztal_Row), 8, q)

def move_bluejay(board,b,row,col):
    BlueJay_Row = [-1, -1, 1, 1]
    BlueJay_Col = [-1, 1, 1, -1]
    moveBird(board, row, col, BlueJay_Row, BlueJay_Col, len(BlueJay_Row), 8, b)

def move_robin(board,r,row,col):
    Robin_Row = [0, -1, 0, 1]
    Robin_Col = [-1, 0, 1, 0]
    moveBird(board, row, col, Robin_Row, Robin_Col, len(Robin_Row), 8, r)

def move_kingfisher(board,k,row,col):
    KingFisher_Row = [1, 1, 1, 0, -1, -1, -1, 0]
    KingFisher_Col = [-1, 0, 1, 1, 1, 0, -1, -1]
    moveBird(board, row, col, KingFisher_Row, KingFisher_Col, len(KingFisher_Row), 2, k)

def move_nighthawk(board,n,row,col):
    NightHawk_Row = [1, 2, 2, 1, -1, -2, -2, -1]
    NightHawk_Col = [-2, -1, 1, 2, 2 ,1, -1, -2]
    moveBird(board, row, col, NightHawk_Row, NightHawk_Col, len(NightHawk_Row), 2, n)

def aplha_beta_decision(initial_board,player):
    #generatesuccessor(initial_board,player)#comment and uncomment aplha beta algo
    maxi = -9999
    state = []
    for successor in generatesuccessor(initial_board,player):
         beta = mini_value(successor,1,-9999,9999,not player)
         if(maxi < beta):
            state = successor
            maxi = beta
    return state

def max_value(state,depth,alpha,beta,player):
    if(depth == maxdepth):
        return evaluation_function(state)
    else:
        for successor in generatesuccessor(state,player):
            alpha = max(alpha,mini_value(successor,depth+1,alpha,beta,not player))
            if(alpha >= beta):
                return alpha
    return alpha

def mini_value(state,depth,alpha,beta,player):

    if(depth == maxdepth):
        return evaluation_function(state)
    else:
        for successor in generatesuccessor(state,player):
            beta = min(alpha,max_value(successor,depth+1,alpha,beta,not player))
            if(beta <= alpha):
                return beta
    return beta

def evaluation_function(board):
    print("Do evaluation function")
    pass

def identify_opponent(player):
    global me
    global opposition

    if player == True:
        me = white
        opposition = black
    else:
        me = black
        opposition = white

def create_board(initial_state):
    board = list();
    for j in range(0,63,8):
        board.append(list(initial_state[j:j+8]))
    return board

def read_input():
    turn = sys.argv[1]
    initial_state = sys.argv[2]
    time = int(sys.argv[3])
    return (turn,initial_state,time)

def main():
    (turn,initial_state,time) = read_input()
    if (len(initial_state) != 64):
        print(len(initial_state))
        return -1
    inital_board = create_board(initial_state)
    print("***** inital_board****************")
    printable_board(inital_board)
    print("********************************")
    if turn == 'w':
        player = True
    else:
        player = False

    aplha_beta_decision(inital_board,player)

if __name__=="__main__":
    main()
