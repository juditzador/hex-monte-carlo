#!/usr/bin/python

import random, copy
import numpy as np
import pickle


# Run Monte-Carlo simulations of Hex.

# TODO:
# -- Implement Gale's algorithm for determining who wins a filled board
# -- Generate random Hex boards (Ramsey, Standard, and Symmetric)

# the standard board structure:
#    boards are n x n lists of lists, with each entry being '1'st player or '2'nd player
#    1st player connects vertically, 2nd player horizontally

# the board convention

#    22222
#  1 o-o-o 1
#  1 |/|/| 1
#  1 o-o-o 1
#  1 |/|/| 1
#  1 o-o-o 1
#    22222

#  the indexing convention

# [y][x] = [y,x]

#   ----------> 
# | 0,0 0,1 0,2
# | 1,0 1,1 1,2
# v 2,0 2,1 2,2
#               

# example boards

# 1st player wins
example_first_a  = [[1,1,1],
                    [1,1,1],
                    [1,1,1]];

# 2nd player wins
example_second_a  = [[2,2,2],
                     [2,2,2],
                     [2,2,2]];
 
def extend(board):
    """ Mark the edges of the board with stones denoting who needs to connect.
        This creates the border of stones used in Gale's Algorithm. 

                    21111
        a b c       2abc2
        e f g ----> 2efg2
        h i j       2hij2
                    11112
        
        This convention dictates: 
            -- 2nd plays horizontally
            -- 1st plays vertically
    """

    sideLength = len(board);

    extended_board = [];

    first_row = [2] + ( [1] * (sideLength + 1) )
    extended_board.append(first_row);

    for row in board:
        middle_row = [2] + row + [2];
        extended_board.append(middle_row);

    last_row = ([1] * (sideLength + 1) ) + [2];
    extended_board.append(last_row);

    return extended_board;
 
def printBoard(board):
    """ Print a nice grid layout of the board """
    for row in board:
        print("  ".join(map(str,row)));

def onBoard(v,n):
    """ Given a vector, determine if it is on the board. """
    if ((-1 <= v[0] <= n + 1) and (0 <= v[1] <= n + 1)): 
        return True;
    else:
        return False;

def Gale(board):
    """ Given a filled board, return the winner. """
    xBoard = extend(board);
    sideLength = len(board[0]);
    v2_chain = []
    v3_chain = []

    # the four vertices in Gale's Algorithm
    # 
    #           v1  [-1,1]    wraps to the bottom
    #          / |
    #         /  |
    #        /   |
    #       /    |
    #[0,0] v2-|-v3 [0,1]      0,0 is the top right on xBoard
    #      |  v  /
    #      |    /
    #      |   /
    #      |  /
    #       v4 [1,0]
    #
    # note: left and right are reversed, since we head along the arrow

    v1 = np.array([-1,1]);
    v2 = np.array([0,0]);
    v3 = np.array([0,1]);
    v4 = np.array([1,0]);
    
    while (onBoard(v4, sideLength)):
        v1_new = np.array
        v2_new = np.array
        v3_new = np.array
        v4_new = np.array

        # PRINT the edge just passed
        #print("\t {0}-{1}".format(str(v2), str(v3)))
        
        # do not append sides to the chain
        if (0 < v2[0] < sideLength + 1) and (0 < v2[1] < sideLength + 1):  # v2 is not on the boarder
            v2_chain.append([v2[0]-1, v2[1]-1])  # not in xBoard, but in board coordinates
        if (0 < v3[0] < sideLength + 1) and (0 < v3[1] < sideLength + 1):  # v2 is not on the boarder
            v3_chain.append([v3[0]-1, v3[1]-1])  # not in xBoard, but in board coordinates
        
        if xBoard[v4[0]][v4[1]] == xBoard[v3[0]][v3[1]]:
            # go left 
            v1_new = copy.deepcopy(v3)
            v2_new = copy.deepcopy(v2)
            v3_new = copy.deepcopy(v4)
            v4_new = copy.deepcopy(v2 + (v2 - v1))
        elif xBoard[v4[0]][v4[1]] == xBoard[v2[0]][v2[1]]:
            # go right
            v1_new = copy.deepcopy(v2)
            v2_new = copy.deepcopy(v4)
            v3_new = copy.deepcopy(v3)
            v4_new = copy.deepcopy(v3 + (v3 - v1))
        else:
            print('no decision')
        
        v1,v2,v3,v4=v1_new,v2_new,v3_new,v4_new
  
    # [n,-1] = bottom left
    # if v4 exits the bottom left corner, then `1'st won
    if v4[1] == -1:
        return 1, list(set(map(tuple,v3_chain)))
    # [0,n] = top right
    # if v4 exits the top right corner, then `2'nd won
    elif v4[0] == 0:
        return 2, list(set(map(tuple,v2_chain)))
    else:
       raise ValueError('The Gale algorithm broke: not [* -1] or [0 *].')
        
def BernoulliRandomBoard(sidelength):
    """ Produces a filled board by tossing a fair {1,2}-coin for each cell. """

    board = [[random.choice([1,2]) for x in range(0, sidelength)] for x in range(0,sidelength)];

    return(board);

### Try out Gale on random boards ###

#for i in range(1,2):
#    board = BernoulliRandomBoard(2)
#    printBoard(board)
#    print(Gale(board))
#    print(Gale(np.rot90(board, 2).tolist()))
#    printBoard(board)

#### Simulator ####

N = 1000;

halfBoardSize = 15;
BoardSize = 2*halfBoardSize + 1


print("Simulating {0}x{0} with N={1} trials".format(BoardSize,N));

max_location = []  # location of the critical point
max_location_val = []  # coin flip outcome at max_location
win1_history = []  # probability of player 1 winning in a round (board scenario)
max_val_history = []  # accumulated critical point values, normalized by N
win_margin_history = []  # difference between best cirtical point and the second one, normalized by N

for step in range(BoardSize * BoardSize):
    criticalCount = np.zeros((BoardSize, BoardSize));
    win1 = 0
    for i in range(N):
        board = BernoulliRandomBoard(BoardSize);
        
        for val, ml in enumerate(max_location):
            board[ml[0]][ml[1]] = max_location_val[val]
        
        winner, chain = Gale(board)
        if winner == 1:
            win1 += 1
        rot_winner, rot_chain = Gale(np.rot90(board, 2).tolist())
        
        # need to rotate the rot_chain elements back to the original coordinate system
        rot_chain = list(map(list,rot_chain))
        for rc in rot_chain:
            rc[0], rc[1] = BoardSize - 1 - rc[0], BoardSize - 1 - rc[1] 
        rot_chain = list(set(map(tuple,rot_chain)))

        # find common elements
        critical_fields = set(chain).intersection(rot_chain)

        for field in critical_fields:
            criticalCount[field[0]][field[1]] += 1;  
            
        # delete fixed points from criticalCount
        for ml in max_location:
            criticalCount[ml[0]][ml[1]] = 0

    #print(criticalCount)
    if not criticalCount.any():
        print(f'Game over after {step} rounds.')
        break
    else:
        max_val = np.max(criticalCount)
        sec_max_val = criticalCount.sort()[1]  # second element
        win_margin_history,append((max_val - sec_max_val) / max_val)
        max_x = np.unravel_index(np.argmax(criticalCount), criticalCount.shape)[0]
        max_y = np.unravel_index(np.argmax(criticalCount), criticalCount.shape)[1]
        max_location.append([max_x, max_y])
        max_location_val.append(random.choice([1,2]))  # fixing it to 1 or 2 for next round
        win1_history.append(win1/N)
        max_val_history.append(max_val / N)
        print(f'The maximum is at {max_location[-1]} with value {max_val}, fixing to {max_location_val[-1]}. Player 1 won {win1} times out of {N} games.')
        
        
board_pattern = np.zeros((BoardSize, BoardSize));
for val, ml in enumerate(max_location):
    board_pattern[ml[0]][ml[1]] = max_location_val[val]
print(board_pattern)
np.savetxt('walk.out', np.rot90(board_pattern, 1).astype(int), fmt='%i', delimiter=' ')
np.savetxt('walk_readable.out', board_pattern.astype(int), fmt='%i', delimiter=' ')
np.savetxt('walk_path.out', max_location, fmt='%i', delimiter=' ')
np.savetxt('walk_path_val.out', max_location_val, fmt='%i', delimiter=' ')
np.savetxt('win1.out', win1_history, fmt='%f', delimiter=' ')
np.savetxt('max_val.out', max_val_history, fmt='%f', delimiter=' ')
np.savetxt('par.out', [BoardSize, N, step], fmt='%i', delimiter=' ')
np.savetxt('margin.out', win_margin_history, fmt='%f', delimiter=' ')
