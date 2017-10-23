#!/usr/bin/python2.7
'''
The program is similar to the classical chess game apart from the stated rules that there wont be en passant,
castling and check/checkmates. Following is the abstraction model that we followed.
    Initial State: 8 * 8 board configuaration given in one line provide by user.
    Successor Function: Board configuration represented as every possible movement of a piece (Parakeeth, Robin,
                        BlueJay, Night, Quetzal and Kingfisher).
    Cost function: There is not cost function involved. Either player should win or loose.

Program accepts three command line parameters:
1) Players turn
2) Intial board configuration
3) Time within which next move the program should output.
The board configuration is saved as a 2-d array with top two row occupied by white birds and last two rows by black birds
`player` bool variable is passed throughout the program, True value is used for players {White | Black} turn given as user
input and False value represents other player {Black | White}.

The program plays against the opponent, evaluates the board state at depth 4 using material evaluation (heuristic) function.

Algorithm used for generating optimal move.
-> Alpha Beta Pruning: As a result of evaluating the state of board at depth = 4, it can be found that a portion of the search
tree can be ignored as no further evaluations can guarantee better results. This can happen because white and black area
against one another. White plays what is best for it and black plays what is best for it, so it would make sense for white
to ignore any portion of the tree where black has a clear upperhand that it can choose to play.
NOTE: If black is the player turn provided by user then, material function value is multiplied by -1 so the evaluation
rules are negated from white to black.
-> Visited Array: Often, two different pathways, in a search tree can result in the same board being evaluated. Instead of
repeating the same calculations again, the program stores a table of values in a dictionary where keys are string format of
2-d board configuration. This is similar to dynamic programming approach called `memoization`.

In order to walk in the tree to seach an optimal result, program should know to evaluate board configuration to decide
which player has advantage over other. Hence, two evaluation functions are used:
-> Material evaluation function: Each piece (White and Black) has a value and the more pieces you have, the better off your
                                 position is likely to be. For example, if white has an extra queen, it has an advantage
                                 over black. The program assumes best play from either side as it traverses up the search
                                 tree and chooses the best move to be played. A problem that will arise is the number of
                                 postions that need to be evaulated. Even at 4 levels of depth, thousands of positions have
                                 to be evaluatd. This function is effective since the game will follow a defensive come
                                 attacking strategy, i.e the function will prevent form loosing user pieces based on weight
                                 and attack again based on how much worth will it be to capture opponent piece.
-> King capture: Min_value and Max_value checks whether its king is captured. If MAX node king is captured alpha value of
                 -INFINITY is retured depicting that MAX (user) will( or has lost )the game and +INFINITY by MIN saying
                  user has (or will) the game.

Challenges
The trade-off between depth and time was the most challenging task which we had to face. When BlueJay,Queztal and Robin
were out in the center the number of successors were many and expanding each of the successors was time consuming. Inorder to
overcome this problem we generated successors based on their evaluation function values. Successors for each piece
which had the maximum(max turn)/mininum(min turn) evaluation function value were taken for the next depth.Thereby decreasing
the number of successors generated. We also came up with memoization technique where in we evaluate the board only once and
stored it in a dictionary and this can be used to get evaluation function for the subsequent calls. This reduce the time
required for expansion of the successors. Memoization came out to be the better solution for this problem.

Improvements
Although dynamic programming is reducing the running time, for some board configuration the running time is still high.
Once soluion to this problem is to reduce the depth and have a stronger evaluation function. Material evaluation function
simply counts the number of pieces and plays a defensive game. While calculating the favourability of a board the postion
of each of the piece should also be taken into consideration. For example, NightHawk has many options when in the center
of the board than in the corners and its weight can be increased..Certain board configurations such as the one where
there are two BlueJays are more favorable since they cover both black and white squares.Improvements to the evaluation
function gives the freedom of decreasing the depth thereby decreasing the running time.

Pruning can be also improved by generating the successors in certain order such a way the alpha becomes greater than beta
without traversing many successors in our game tree.

Another way to handle time limit would be to use Iterative Depth First Search where we store the best possible move at
each depth and we return the best possible move at the maximum depth we reached before the time limit expires.
'''

import sys
import copy

INF = 99999999999
MAXDEPTH = 4
WHITE = ['P','R','B','Q','K','N'];
BLACK = ['p','r','b','q','k','n'];
# MATERIAL Weight
PIECE_WEIGHT = {
    'P': 1, 'p': -1, 'R': 5, 'r': -5, 'B': 3, 'b': -3, 'N': 3, 'n': -3, 'Q': 9, 'q': -9, 'K': 100, 'k': -100
}

# An array representing opponent player array (White or Black)
opposition = []
# Data structure used to store possible successor from a given state
frontier = []
# Visited array storing values of a state visited.
visited = {}

# Print Human readable board format
def printable_board(board):
    for row in board:
        print(row)
    print("--------------------------------------------------------------------------------------")
    pass

# Check whether a parakeeth can be placed in (row, col)
def isValidForParakeeth(board, row, col, i, player):
    if (row >= 0 and row <= 7 and col >= 0 and col <= 7):
        if i == 3:
            if(player):
                if board[row - 1][col] == "." and board[row][col] == "." and row - 2 == 1:
                    return True
            else:
                if board[row + 1][col] == "." and board[row][col] == "." and row + 2 == 6:
                    return True
        elif i % 2 == 0 and board[row][col] in opposition:
            return True
        elif i == 1 and board[row][col] == ".":
            return True
    return False

# Check whether any piece from (Robin, Bluejay, Night, Queen and King) can be placed in (row, col)
# Disable a move of respective piece if another blocks its way (row_list/col_list*=100)
def isValidorDisbale(board, row, col, row_list, col_list, i):
    if (row >= 0 and row <= 7 and col >= 0 and col <= 7):
        if board[row][col] == ".":
            return True
        row_list[i] *= 100; col_list[i] *= 100
        if board[row][col] in opposition:
            return True
        else:
            return False

# Generate all possible moves from each piece given a board of a player
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
                move_quetzal(board, q, row, col)
            elif(board[row][col] == k):
                move_kingfisher(board, k, row, col)
            elif(board[row][col] == n):
                move_nighthawk(board, n, row, col)
    return frontier

# Return a new board with piece added at (row, col)
def add_piece(board, row, col, piece):
    return board[0:row] + [board[row][0:col] + [piece,] + board[row][col+1:]] + board[row+1:]

# Move Parakeeth at (row, col)
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
        if (isValidForParakeeth(board, row1, col1, i, p in WHITE)):
            new_board = add_piece(board, row, col, ".")
            if(row1 == 0 or row1 == 7):
                new_board = add_piece(new_board, row1, col1, q)
            else:
                new_board = add_piece(new_board, row1, col1, p)
            frontier.append(new_board)

# Generic function to move a bird from (row, col) to (row1, col1)
def moveBird(board, row, col, possible_row, possible_col, possible_moves, iterations, bird):
    for i in range(possible_moves):
        for j in range(1, iterations):
            row1 = row + possible_row[i] * j
            col1 = col + possible_col[i] * j
            if (isValidorDisbale(board, row1, col1, possible_row, possible_col, i)):
                new_board = add_piece(board, row, col, ".")
                new_board = add_piece(new_board, row1, col1, bird)
                frontier.append(new_board)

# Build each move for Quetzal starting from (row+0, col+0).
# . .    .       .     .      . . .
# . .    .       .     .      . . .
# . .    .       .     .      . . .
# . . (+1,-1) (+1,+0) (+1,+1) . . .
# . . (+0,-1) (+0,+0) (+0,+1) . . .
# . . (-1,-1) (-1,+0) (-1,+1) . . .
# . .    .       .     .      . . .
# . .    .       .     .      . . .
def move_quetzal(board, q, row, col):
    Queztal_Row = [1, 1, 1, 0, -1, -1, 0, -1]
    Queztal_Col = [1, 0,-1, 1, -1, 0, -1, 1]
    moveBird(board, row, col, Queztal_Row, Queztal_Col, len(Queztal_Row), 8, q)

# Build each move for Bluejay
def move_bluejay(board, b, row, col):
    BlueJay_Row = [-1, -1, 1, 1]
    BlueJay_Col = [-1, 1, 1, -1]
    moveBird(board, row, col, BlueJay_Row, BlueJay_Col, len(BlueJay_Row), 8, b)

# Build each move for Robin
def move_robin(board, r, row, col):
    Robin_Row = [0, -1, 0, 1]
    Robin_Col = [-1, 0, 1, 0]
    moveBird(board, row, col, Robin_Row, Robin_Col, len(Robin_Row), 8, r)

# Build each move for KingFisher
def move_kingfisher(board, k, row, col):
    KingFisher_Row = [1, 1, 1, 0, -1, -1, -1, 0]
    KingFisher_Col = [-1, 0, 1, 1, 1, 0, -1, -1]
    moveBird(board, row, col, KingFisher_Row, KingFisher_Col, len(KingFisher_Row), 2, k)

# Build each move for Nighthawk
def move_nighthawk(board, n, row, col):
    NightHawk_Row = [1, 2, 2, 1, -1, -2, -2, -1]
    NightHawk_Col = [-2, -1, 1, 2, 2 ,1, -1, -2]
    moveBird(board, row, col, NightHawk_Row, NightHawk_Col, len(NightHawk_Row), 2, n)

# Check whether king is captured
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

# Alpha beta pruning algorithm
def alpha_beta_decision(initial_board, player):
    maxi = -INF
    state = []
    for successor in generatesuccessor(initial_board, player):
        beta = mini_value(successor, 1, -INF, INF, not player)
        if(maxi <= beta):
            state = successor
            maxi = beta
    return state

# Generate Max nodes (favourable moves for user)
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

# Generate Min nodes (worst moves for user)
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

# Material Heuristic evaluation function calculating based on bird weights
def material_evaluation(board):
    value = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col] != '.':
                value += PIECE_WEIGHT[board[row][col]]
    return value

# Identify the opponent type
def identify_opponent(player):
    global opposition

    if player == True:
        opposition = BLACK
    else:
        opposition = WHITE

# Create a board as a 2-d array
def create_board(initial_state):
    board = list();
    for j in range(0,63,8):
        board.append(list(initial_state[j:j+8]))
    return board

# Read input from command linen parameters
def read_input():
    if (len(sys.argv)<4):
        print ("Please enter three inputs.\n1.Player turn (w 'or' b)\n2.Board configuration\
                \n3.Time (in seconds) for algorithm to run.\nExiting...")
        sys.exit(0)
    turn = sys.argv[1]
    initial_state = sys.argv[2]
    time = int(sys.argv[3])
    return (turn, initial_state, time)

# Validate input from command linen parameters
def validate_input(initial_state, turn):
    if (len(initial_state) != 64):
        print ("Please enter valid board... Exiting...")
        return -1
    if not turn in ('w', 'b'):
        print ("Please enter valid player (w 'or' b) turn... Exiting...")
        return -1

# Main function driving the program
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
