#!/usr/bin/python2.7
import sys
import copy

INF = 99999999999
MAXDEPTH = 4
WHITE = ['P','R','B','Q','K','N'];
BLACK = ['p','r','b','q','k','n'];
PIECE_WEIGHT = {
    'P': 1, 'p': -1, 'R': 5, 'r': -5, 'B': 3, 'b': -3, 'N': 3, 'n': -3, 'Q': 9, 'q': -9, 'K': 100, 'k': -100
}

opposition = []
frontier = []
visited = {}

def printable_board(board):
    for row in board:
        print(row)
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

def generatesuccessor(board, player):
    global frontier
    frontier = []
    identify_opponent(player)

    if player:
        (p, r, b, q, k, n) = WHITE
    else:
        (p, r, b, q, k, n) = BLACK

    for row in range(0, 8):
        for col in range(0, 8):
            if(board[row][col] == p):
                move_parakeeth(board, p, row, col)
            elif(board[row][col] == r):
                move_robin(board, r, row, col)
            elif(board[row][col] == b):
                move_bluejay(board, b, row, col)
            elif(board[row][col] == q):
                move_queztal(board, q, row, col)
            elif(board[row][col] == k):
                move_kingfisher(board, k, row, col)
            elif(board[row][col] == n):
                move_nighthawk(board, n, row, col)
    return frontier

def add_piece(board, row, col, piece):
    return board[0:row] + [board[row][0:col] + [piece,] + board[row][col+1:]] + board[row+1:]

def move_parakeeth(board, p, row, col):
    if p in BLACK:
        q = 'q'
        Parakeeth_Row = [-1, -1, -1]
        if row == 6:
            Parakeeth_Row.append(-2)
    else:
        q = 'Q'
        Parakeeth_Row = [1, 1, 1]
        if row == 1:
            Parakeeth_Row.append(2)

    Parakeeth_Col = [-1, 0, 1, 0]

    for i in range(0, len(Parakeeth_Row)):
        row1 = row + Parakeeth_Row[i]
        col1 = col + Parakeeth_Col[i]
        if (isValidForParakeeth(board, row1, col1, i)):
            new_board = add_piece(board, row, col, ".")
            if(row1 == 0 or row1 == 7):
                new_board = add_piece(new_board, row1, col1, q)
            else:
                new_board = add_piece(new_board, row1, col1, p)
            frontier.append(new_board)

def moveBird(board, row, col, possible_row, possible_col, possible_moves, iterations, bird):
    for i in range(possible_moves):
        for j in range(1, iterations):
            row1 = row + possible_row[i] * j
            col1 = col + possible_col[i] * j
            if (isValidorDisbale(board, row1, col1, possible_row, possible_col, i)):
                new_board = add_piece(board, row, col, ".")
                new_board = add_piece(new_board, row1, col1, bird)
                frontier.append(new_board)

def move_queztal(board, q, row, col):
    Queztal_Row = [1, 1, 1, 0, -1, -1, 0, -1]
    Queztal_Col = [1, 0,-1, 1, -1, 0, -1, 1]
    moveBird(board, row, col, Queztal_Row, Queztal_Col, len(Queztal_Row), 8, q)

def move_bluejay(board, b, row, col):
    BlueJay_Row = [-1, -1, 1, 1]
    BlueJay_Col = [-1, 1, 1, -1]
    moveBird(board, row, col, BlueJay_Row, BlueJay_Col, len(BlueJay_Row), 8, b)

def move_robin(board, r, row, col):
    Robin_Row = [0, -1, 0, 1]
    Robin_Col = [-1, 0, 1, 0]
    moveBird(board, row, col, Robin_Row, Robin_Col, len(Robin_Row), 8, r)

def move_kingfisher(board, k, row, col):
    KingFisher_Row = [1, 1, 1, 0, -1, -1, -1, 0]
    KingFisher_Col = [-1, 0, 1, 1, 1, 0, -1, -1]
    moveBird(board, row, col, KingFisher_Row, KingFisher_Col, len(KingFisher_Row), 2, k)

def move_nighthawk(board, n, row, col):
    NightHawk_Row = [1, 2, 2, 1, -1, -2, -2, -1]
    NightHawk_Col = [-2, -1, 1, 2, 2 ,1, -1, -2]
    moveBird(board, row, col, NightHawk_Row, NightHawk_Col, len(NightHawk_Row), 2, n)

def iskingcaptured(board, player):
    if(player):
        king = 'K'
    else:
        king = 'k'
    for row in range(0, 8):
        for col in range(0, 8):
            if(board[row][col] == king):
                return False
    return True

def alpha_beta_decision(initial_board, player):
    maxi = -INF
    state = []
    for successor in generatesuccessor(initial_board, player):
        beta = mini_value(successor, 1, -INF, INF, not player)
        if(maxi <= beta):
            state = successor
            maxi = beta
    return state

def max_value(state, depth, alpha, beta, player):
    if(iskingcaptured(state, player)):
        return -INF

    if(depth == MAXDEPTH ):
        if(player):
            return material_evaluation(state)
        else:
            return -1 * material_evaluation(state)
    else:
        for successor in generatesuccessor(state, player):
            if str(successor) in visited:
                alpha = visited[str(successor)]
            else:
                alpha = max(alpha, mini_value(successor, depth + 1, alpha, beta, not player))
                visited[str(successor)] = alpha
            if(alpha >= beta):
                return alpha
    return alpha

def mini_value(state, depth, alpha, beta, player):

    if(iskingcaptured(state, player)):
        return INF

    if(depth == MAXDEPTH):
        if(player):
            return material_evaluation(state)
        else:
            return -1 * material_evaluation(state)
    else:
        for successor in generatesuccessor(state, player):
            if str(successor) in visited:
                beta = visited[str(successor)]
            else:
                beta = min(beta, max_value(successor, depth + 1, alpha, beta, not player))
                visited[str(successor)] = beta
            if(alpha >= beta):
                return beta
    return beta

def material_evaluation(board):
    value = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col] != '.':
                value += PIECE_WEIGHT[board[row][col]]
    return value

def identify_opponent(player):
    global opposition

    if player == True:
        opposition = BLACK
    else:
        opposition = WHITE

def create_board(initial_state):
    board = list();
    for j in range(0,63,8):
        board.append(list(initial_state[j:j+8]))
    return board

def read_input():
    if (len(sys.argv)<4):
        print ("Please enter three inputs.\n1.Player turn (w 'or' b)\n2.Board configuration\
                \n3.Time (in seconds) for algorithm to run.\nExiting...")
        sys.exit(0)
    turn = sys.argv[1]
    initial_state = sys.argv[2]
    time = int(sys.argv[3])
    return (turn, initial_state, time)

def validate_input(initial_state, turn):
    if (len(initial_state) != 64):
        print ("Please enter valid board... Exiting...")
        return -1
    if not turn in ('w', 'b'):
        print ("Please enter valid player (w 'or' b) turn... Exiting...")
        return -1

def main():
    (turn, initial_state, time) = read_input()
    inital_board = create_board(initial_state)
    print("\n********************************** INITIAL BOARD **************************************")
    printable_board(inital_board)
    print("**************************************************************************************\n")
    if turn == 'w':
        player = True
    else:
        player = False

    next_move = alpha_beta_decision(inital_board, player)

    print("\n*********************************** FINAL BOARD **************************************")
    printable_board(next_move)
    print("**************************************************************************************\n")
    next_move_str = ''
    for row in range(0, 8):
        for col in range(0, 8):
            next_move_str += next_move[row][col]
    print(next_move_str)

if __name__=="__main__":
    main()
