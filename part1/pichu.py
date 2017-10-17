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


def generatesuccessor(board):
    printable_board(board)
    for i in range(0,8):
        for j in range(0,8):
            '''if(board[i][j] == 'P'):
                move_parakeeth(board,i,j)'''
            '''if(board[i][j] == 'R'):
                move_robin(board,i,j)'''
            '''if(board[i][j] == 'B'):
                move_bluejay(board,i,j)'''
            if(board[i][j] == 'Q'):
                move_queztal(board,i,j)
            '''elif(board[i][j] == 'K'):
                move_kingfisher(board,i,j)
            elif(board[i][j] == 'N'):
                move_nighthawk(board,i,j)'''


def move_vertical(board,piece,row,col):
    possible_moves = [1,2,3,4,5,6,7]
    print(row,col)
    for i in possible_moves:
        if(row+i <= 7):
            if(board[row+i][col] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row+i][col]
                new_board[row][col] = "."
                new_board[row+i][col] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break

    for i in possible_moves:
        if(row-i >=0):
            if(board[row-i][col] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row-i][col]
                new_board[row][col] = "."
                new_board[row-i][col] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break

def move_hortizontal(board,piece,row,col):
    possible_moves = [1,2,3,4,5,6,7]
    for i in possible_moves:
        if(col+i <= 7 ):
            if(board[row][col+i] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row][col+i]
                new_board[row][col] = "."
                new_board[row][col+i] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break
    for i in possible_moves:
        if(col-i >=0):
            if(board[row][col-i] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row][col-i]
                new_board[row][col] = "."
                new_board[row][col-i] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break


def move_diagonal(board,piece,row,col):
    possible_moves = [1,2,3,4,5,6,7]
    for i in possible_moves:
        if(row+i<=7 and col+i <=7):
            if(board[row+i][col+i] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row+i][col+i]
                new_board[row][col] = "."
                new_board[row+i][col+i] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break
    for i in possible_moves:
        if(row-i>=0 and col-i>=0):
            if(board[row-i][col-i] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row-i][col-i]
                new_board[row][col] = "."
                new_board[row-i][col-i] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break

    for i in possible_moves:
        if(row-i >=0 and col+i<=7):
            if(board[row-i][col+i] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row-i][col+i]
                new_board[row][col] = "."
                new_board[row-i][col+i] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break

    for i in possible_moves:
        if(row+i <=7 and col-i>=0):
            if(board[row+i][col-i] not in white):
                new_board = copy.deepcopy(board)
                current_piece = board[row+i][col-i]
                new_board[row][col] = "."
                new_board[row+i][col-i] = piece
                printable_board(new_board)
                frontier.append(new_board)
                if(current_piece in black):
                    break
            else:
                break


def move_parakeeth(board,row,col):#not checking for quezals and first move
    print(row,col)
    if(row+1 <=7 and col+1<=7 ):
        if(board[row+1][col+1] in black):
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row+1][col+1] = "P"
            printable_board(new_board)
            frontier.append(new_board)

    if(row+1 <=7 and col-1>=0 ):
        if(board[row+1][col-1] in black):
            new_board = copy.deepcopy(board)
            new_board[row][col] = "."
            new_board[row+1][col-1] = "P"
            printable_board(new_board)
            frontier.append(board)

    if(row+1 <=7):
        if(board[row+1][col] not in white):
            new_board = copy.deepcopy(board)
            new_board[row][col] = "."
            new_board[row+1][col] = "P"
            printable_board(new_board)
            frontier.append(new_board)


def move_robin(board,row,col):
    move_vertical(board,'R',row,col)
    move_hortizontal(board,'R',row,col)

def move_queztal(board,row,col):
    move_vertical(board,'Q',row,col)
    move_hortizontal(board,'Q',row,col)
    move_diagonal(board,'Q',row,col)

def move_bluejay(board,row,col):
    move_diagonal(board,'R',row,col)

def move_kingfisher(board,row,col):
    pass

def move_nighthawk(board,row,col):
    pass

def idfs(initial_board):
    generatesuccessor(initial_board)
    #for i in frontier:
    #    print(i)

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
