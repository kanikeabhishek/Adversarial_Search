#!/usr/bin/python2.7
import sys
import copy


white = ['P','R','B','Q','K','N'];
black = ['p','r','b','q','k','n'];

# `me` not in use now can be removed or used later.
me = []

opposition = []

frontier = []
maxdepth = int(sys.argv[4])

def printable_board(board):
    for i in board:
        print(i)
    print("--------------------------------------------------------------------------------------")
    pass

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
        if board[row][col] in opposition:
            return True
        else:
            return False

def generatesuccessor(board,player):
    global frontier
    frontier = []
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

    if p in black:
        q= 'q'
        Parakeeth_Row = [-1, -1, -1, -2]
    else:
        q= 'Q'
        Parakeeth_Row = [1, 1, 1, 2]

    Parakeeth_Col = [-1, 0, 1, 0]

    for i in range(0, len(Parakeeth_Row)):
        row1 = row + Parakeeth_Row[i]
        col1 = col + Parakeeth_Col[i]
        if (isValidForParakeeth(board, row1, col1, i)):
            new_board = copy.deepcopy(board)
            new_board[row][col] = "."
            if(row1 == 0 or row1 == 7):
                new_board[row1][col1] = q
            else:
                new_board[row1][col1] = p
            frontier.append(new_board)

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
    # generatesuccessor(initial_board,player)#comment and uncomment aplha beta algo
    maxi = -99999999999
    state = []
    for successor in generatesuccessor(initial_board, player):
         beta = mini_value(successor, 1, -99999999999, 99999999999, not player)
         if(maxi < beta):
            state = successor
            maxi = beta
    return state

def max_value(state,depth,alpha,beta,player):
    if(depth == maxdepth):
        return piece_square_evaluation(state)
    else:
        for successor in generatesuccessor(state, player):
            alpha = max(alpha,mini_value(successor, depth+1, alpha, beta, not player))
            if(alpha >= beta):
                return alpha
    return alpha

def mini_value(state,depth,alpha,beta,player):

    if(depth == maxdepth):
        return piece_square_evaluation(state)
    else:
        for successor in generatesuccessor(state, player):
            beta = min(beta,max_value(successor, depth+1, alpha, beta, not player))
            if(alpha >= beta):
                return beta
    return beta

def kingPosistions(board):
    for i in range(0,8):
        for j in range(0,8):
            if (board[i][j] == 'K'):
                king_white = (i,j)
            if (board[i][j] == 'k'):
                king_black = (i,j)
    return (king_white, king_black)

def material_evaluation(board):
    value = 0
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] == 'P':
                value += 1
            if board[i][j] == 'p':
                value -= 1
            if board[i][j] == 'R':
                value += 5
            if board[i][j] == 'r':
                value -= 5
            if board[i][j] == 'B':
                value += 3
            if board[i][j] == 'b':
                value -= 3
            if board[i][j] == 'N':
                value += 3
            if board[i][j] == 'n':
                value -= 3
            if board[i][j] == 'Q':
                value += 9
            if board[i][j] == 'q':
                value -= 9
            if board[i][j] == 'K':
                value += 100
            if board[i][j] == 'k':
                value -= 100
    return value

piece_square_table = {
    'P': [[[0,  0,  0,  0,  0,  0,  0,  0],
         [50, 50, 50, 50, 50, 50, 50, 50],
         [10, 10, 20, 30, 30, 20, 10, 10],
         [5,  5, 10, 25, 25, 10,  5,  5],
         [0,  0,  0, 20, 20,  0,  0,  0],
         [5, -5,-10,  0,  0,-10, -5,  5],
         [5, 10, 10,-20,-20, 10, 10,  5],
         [0,  0,  0,  0,  0,  0,  0,  0]], 100],
    'N': [[[-50,-40,-30,-30,-30,-30,-40,-50],
         [-40,-20,  0,  0,  0,  0,-20,-40],
         [-30,  0, 10, 15, 15, 10,  0,-30],
         [-30,  5, 15, 20, 20, 15,  5,-30],
         [-30,  0, 15, 20, 20, 15,  0,-30],
         [-30,  5, 10, 15, 15, 10,  5,-30],
         [-40,-20,  0,  5,  5,  0,-20,-40],
         [-50,-40,-30,-30,-30,-30,-40,-50]], 320],
    'B': [[[-20,-10,-10,-10,-10,-10,-10,-20],
         [-10,  0,  0,  0,  0,  0,  0,-10],
         [-10,  0,  5, 10, 10,  5,  0,-10],
         [-10,  5,  5, 10, 10,  5,  5,-10],
         [-10,  0, 10, 10, 10, 10,  0,-10],
         [-10, 10, 10, 10, 10, 10, 10,-10],
         [-10,  5,  0,  0,  0,  0,  5,-10],
         [-20,-10,-10,-10,-10,-10,-10,-20]], 330],
    'R': [[[0,  0,  0,  0,  0,  0,  0,  0],
         [ 5, 10, 10, 10, 10, 10, 10,  5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [-5,  0,  0,  0,  0,  0,  0, -5],
         [ 0,  0,  0,  5,  5,  0,  0,  0]], 500],
    'Q': [[[-20,-10,-10, -5, -5,-10,-10,-20],
         [-10,  0,  0,  0,  0,  0,  0,-10],
         [-10,  0,  5,  5,  5,  5,  0,-10],
         [-5,  0,  5,  5,  5,  5,  0, -5],
         [0,  0,  5,  5,  5,  5,  0, -5],
         [-10,  5,  5,  5,  5,  5,  0,-10],
         [-10,  0,  5,  0,  0,  0,  0,-10],
         [-20,-10,-10, -5, -5,-10,-10,-20]], 900],
    'K': [[[-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-30,-40,-40,-50,-50,-40,-40,-30],
         [-20,-30,-30,-40,-40,-30,-30,-20],
         [-10,-20,-20,-20,-20,-20,-20,-10],
         [20, 20,  0,  0,  0,  0, 20, 20],
         [20, 30, 10,  0,  0, 10, 30, 20]], 20000]
}

def piece_square_evaluation(board):
    score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            current_piece = board[row][col]
            if current_piece.upper() in piece_square_table.keys():
                if current_piece.istitle():
                    row1 = ( row * -1 ) - 1
                    score += (piece_square_table[current_piece][0][row1][col] * piece_square_table[current_piece][1])
                else:
                    current_piece = current_piece.upper()
                    score -= (piece_square_table[current_piece][0][row][col] * piece_square_table[current_piece][1])
    return score

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
        return -1
    inital_board = create_board(initial_state)
    print("\n********************************** INITIAL BOARD **************************************")
    printable_board(inital_board)
    print("**************************************************************************************\n")
    if turn == 'w':
        player = True
    else:
        player = False

    next_move = aplha_beta_decision(inital_board,player)

    print("\n*********************************** FINAL BOARD **************************************")
    printable_board(next_move)
    print("**************************************************************************************\n")

if __name__=="__main__":
    main()
