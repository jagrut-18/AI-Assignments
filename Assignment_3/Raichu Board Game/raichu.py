#
# raichu.py : Play the game of Raichu
#
# Parth Verma (paverma), Shivam Balajee (shbala), Jagrut Dhirajkumar Chaudhari (jagchau)
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import itertools
import sys
from collections import Counter

sys.setrecursionlimit(3500)
import math
from copy import deepcopy

MAX_DEPTH = 3


def board_to_string(board, N):
    return "\n".join(''.join(board[i:i + N]) for i in range(0, len(board), N))


# Returns all the possible states after performing all the possible moves of a pichu
def pichu_succ(board, n, pos, is_white):
    succ = []
    # Diagonal 1 move
    moves = [(pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1] + 1)] if is_white else [(pos[0] - 1, pos[1] - 1),
                                                                                   (pos[0] - 1, pos[1] + 1)]
    for position in moves:
        r = position[0]
        c = position[1]
        if is_in_bound(n, position) and board[r][c] == '.':
            board_copy = deepcopy(board)
            board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
            if r == (n - 1 if is_white else 0):
                board_copy[r][c] = '@' if is_white else '$'
            yield board_copy
    # Diagonal jump
    jumps = [(pos[0] + 2, pos[1] - 2), (pos[0] + 2, pos[1] + 2)] if is_white else [(pos[0] - 2, pos[1] - 2),
                                                                                   (pos[0] - 2, pos[1] + 2)]
    for i in range(2):
        r = jumps[i][0]
        c = jumps[i][1]
        if is_in_bound(n, jumps[i]) and board[r][c] == '.' and board[moves[i][0]][moves[i][1]] == (
                'b' if is_white else 'w'):
            board_copy = deepcopy(board)
            board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
            board_copy[moves[i][0]][moves[i][1]] = '.'
            if r == (n - 1 if is_white else 0):
                board_copy[r][c] = '@' if is_white else '$'
            yield board_copy


# Returns all the possible states after performing all the possible moves of a pikachu
def pikachu_succ(board, n, pos, is_white):
    # Forward, left or right 1 move
    moves1 = [(pos[0], pos[1] - 1), (pos[0], pos[1] + 1), (pos[0] + 1 if is_white else pos[0] - 1, pos[1])]
    for position in moves1:
        r = position[0]
        c = position[1]
        if is_in_bound(n, position) and board[r][c] == '.':
            board_copy = deepcopy(board)
            board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
            if r == (n - 1 if is_white else 0):
                board_copy[r][c] = '@' if is_white else '$'
            yield board_copy
    # Forward, left or right 2 moves
    moves2 = [(pos[0], pos[1] - 2), (pos[0], pos[1] + 2), (pos[0] + 2 if is_white else pos[0] - 2, pos[1])]
    for i in range(3):
        r = moves2[i][0]
        c = moves2[i][1]
        if is_in_bound(n, moves2[i]) and board[r][c] == '.' and board[moves1[i][0]][moves1[i][1]] == '.':
            board_copy = deepcopy(board)
            board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
            if r == (n - 1 if is_white else 0):
                board_copy[r][c] = '@' if is_white else '$'
            yield board_copy
    # Forward, left or right 1 jump
    for i in range(3):
        r = moves2[i][0]
        c = moves2[i][1]
        if is_in_bound(n, moves2[i]) and board[r][c] == '.' and board[moves1[i][0]][moves1[i][1]].lower() == (
                'b' if is_white else 'w'):
            board_copy = deepcopy(board)
            board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
            board_copy[moves1[i][0]][moves1[i][1]] = '.'
            if r == (n - 1 if is_white else 0):
                board_copy[r][c] = '@' if is_white else '$'
            yield board_copy
    # Forward, left or right 2 jump
    jumps = [(pos[0], pos[1] - 3), (pos[0], pos[1] + 3), (pos[0] + 3 if is_white else pos[0] - 3, pos[1])]
    for i in range(3):
        r = jumps[i][0]
        c = jumps[i][1]
        middle_items = []
        if is_in_bound(n, moves1[i]):
            middle_items.append(board[moves1[i][0]][moves1[i][1]])
        if is_in_bound(n, moves2[i]):
            middle_items.append(board[moves2[i][0]][moves2[i][1]])
        if is_in_bound(n, jumps[i]) and board[r][c] == '.' and any(item == '.' for item in middle_items) and any(
                item in ('bB' if is_white else 'wW') for item in middle_items):
            board_copy = deepcopy(board)
            board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
            board_copy[moves1[i][0]][moves1[i][1]] = '.'
            board_copy[moves2[i][0]][moves2[i][1]] = '.'
            if r == (n - 1 if is_white else 0):
                board_copy[r][c] = '@' if is_white else '$'
            yield board_copy


# Returns all the possible states after performing all the possible moves of a raichu
def raichu_succ(board, n, pos, is_white):
    inc = 1
    row = pos[0]
    col = pos[1]
    item_found = {}
    for i in range(8):
        item_found[i] = []
    indexes_to_check = [True] * 8
    while any(indexes_to_check):
        locations = [(row - inc, col), (row, col - inc), (row + inc, col),
                     (row, col + inc), (row + inc, col + inc),
                     (row - inc, col - inc), (row - inc, col + inc),
                     (row + inc, col - inc)]
        for i in range(8):
            if not indexes_to_check[i]:
                continue
            r = locations[i][0]
            c = locations[i][1]
            if is_in_bound(n, locations[i]):
                if board[r][c] == '.':
                    board_copy = deepcopy(board)
                    board_copy[pos[0]][pos[1]], board_copy[r][c] = board_copy[r][c], board_copy[pos[0]][pos[1]]
                    if r == (n - 1 if is_white else 0):
                        board_copy[r][c] = '@' if is_white else '$'
                    if len(item_found[i]) == 1:
                        board_copy[item_found[i][0][0]][item_found[i][0][1]] = '.'
                    yield board_copy
                else:
                    is_middle_white = board[r][c] in 'wW@'
                    if is_white != is_middle_white:
                        item_found[i].append(locations[i])
                        if len(item_found[i]) > 1:
                            indexes_to_check[i] = False
                    else:
                        indexes_to_check[i] = False
            else:
                indexes_to_check[i] = False
        inc += 1


def successors(board, N, is_white):
    successors = itertools.chain([])
    for i in range(N):
        for j in range(N):
            if board[i][j] == ('w' if is_white else 'b'):
                successors = itertools.chain(successors, pichu_succ(board, N, (i, j), is_white))
            if board[i][j] == ('W' if is_white else 'B'):
                successors = itertools.chain(successors, pikachu_succ(board, N, (i, j), is_white))
            if board[i][j] == ('@' if is_white else '$'):
                successors = itertools.chain(successors, raichu_succ(board, N, (i, j), is_white))
    return successors


def is_in_bound(n, pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < n and pos[1] < n


def board_to_matrix(board, n):
    board_list = []
    for i in range(0, len(board), n):
        board_list.append(list(board[i:i + n]))
    return board_list


def printable_board(board):
    return "\n".join(["".join(row) for row in board])


def is_win_state(board, is_white):
    s = {j for i in board for j in i}
    s = s.difference(['.'])
    if len(s.difference(list('bB$'))) == 0 or len(s.difference(list('wW@'))) == 0:
        return True
    return False


def evaluate_state(board, is_white):
    items = 'wW@' if is_white else 'bB$'

    count_map = Counter()
    for r in board:
        count_map.update(r)

    value = 0
    for k, v in count_map.items():
        if k == 'w' or k == 'b':
            value += (v if k in items else -v)
        if k == 'W' or k == 'B':
            value += (v * 5 if k in items else -(v * 5))
        if k == '@' or k == '$':
            value += (v * 10 if k in items else -(v * 10))
    return value


def maximize(board, N, a, b, is_white, depth):
    if depth > MAX_DEPTH or is_win_state(board, is_white):
        return evaluate_state(board, is_white)

    max_value = -math.inf
    for succ in successors(board, N, is_white):
        value = minimize(succ, N, a, b, (not is_white), depth + 1)
        max_value = max(max_value, value)
        a = max(a, max_value)
        if b <= a:
            break
    return max_value


def minimize(board, N, a, b, is_white, depth):
    if depth > MAX_DEPTH or is_win_state(board, is_white):
        return evaluate_state(board, is_white)

    max_value = math.inf
    for succ in successors(board, N, is_white):
        value = maximize(succ, N, a, b, (not is_white), depth + 1)
        max_value = min(max_value, value)
        b = min(b, max_value)
        if b <= a:
            break
    return max_value

def find_best_move(board, N, player, timelimit):
    board = board_to_matrix(board, N)
    is_white = player == 'w'
    # succ = successors(board, N, is_white)
    # for s in succ:
    #     print(printable_board(s), evaluate_state(s, is_white))
    #     print('************************')
    # return

    max_score = -math.inf
    for succ in successors(board, N, is_white):
        score = maximize(succ, N, -math.inf, math.inf, is_white, 0)
        if score > max_score:
            max_score = score
            yield ''.join(''.join(row) for row in succ)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print()
        print(new_board)
