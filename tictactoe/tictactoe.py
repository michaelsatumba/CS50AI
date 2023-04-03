import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_X = sum(row.count(X) for row in board)
    num_O = sum(row.count(O) for row in board)
    return X if num_X == num_O else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        row = set(board[i])
        if len(row) == 1 and row != {EMPTY}:
            return row.pop()
        col = set([board[j][i] for j in range(3)])
        if len(col) == 1 and col != {EMPTY}:
            return col.pop()
    diag1 = set([board[i][i] for i in range(3)])
    if len(diag1) == 1 and diag1 != {EMPTY}:
        return diag1.pop()
    diag2 = set([board[i][2-i] for i in range(3)])
    if len(diag2) == 1 and diag2 != {EMPTY}:
        return diag2.pop()
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    if not any(EMPTY in row for row in board):
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    curr_player = player(board)
    if curr_player == X:
        best_val = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_val:
                best_val = value
                best_action = action
    else:
        best_val = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_val:
                best_val = value
                best_action = action
    
    return best_action

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

