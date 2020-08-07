from common.eating import can_eat, eat
from common.entities import Board, Field, Player, Ver, Hor
from enum import Enum
from itertools import product


def next_state(board, player, pos, offset):
    '''
    Yield the next board state given the move, or nothing if the move is not
    viable.
    '''
    try:
        new_pos = pos[0] + offset[0], pos[1] + offset[1]
        new_field = board[new_pos]

        if not new_field.piece:
            # if the field to move to is empty, everything's fine
            new = board.copy()
            new[pos], new[new_pos] = new[new_pos], new[pos]
            new.update()
            yield new
        elif new_field.piece.player == -player:
            # if the field to move to is occupied by the opposing player's
            # piece, simulate the jump across it and check the jumped to field
            jump_pos = new_pos[0] + offset[0], new_pos[1] + offset[1]
            jump_field = board[jump_pos]

            if jump_field.piece is None:
                new = board.copy()
                new[pos], new[jump_pos] = new[jump_pos], new[pos]
                new[new_pos] = Field()
                new.update()
                yield new
    except ValueError:
        pass


def possible_moves_for(board, pos):
    '''
    Yield all possible moves from a given position.
    '''
    i, j = pos[0], pos[1]
    piece = board[i, j].piece

    if not piece:
        raise ValueError(f'({i}, {j}) is empty.')

    player = piece.player

    if piece.is_promoted:
        for offset in product([Ver.DOWN, Ver.UP], [Hor.LEFT, Hor.RIGHT]):
            yield from next_state(board, player, pos, offset)
    elif player == Player.W:
        for offset in [(Ver.DOWN, Hor.LEFT), (Ver.DOWN, Hor.RIGHT)]:
            yield from next_state(board, player, pos, offset)
    else: # player == player.B
        for offset in [(Ver.UP, Hor.LEFT), (Ver.UP, Hor.RIGHT)]:
            yield from next_state(board, player, pos, offset)


def possible_moves(board, player, musteat):
    '''
    Yield all possible moves for a given player. An additional parameter is
    given depending on the ruleset of the game (namely, does the player have
    to eat a piece if eating is possible).
    '''
    if musteat:
        eats = []
        for pos in board.fields_of(player):
            eat_pos = can_eat(board, pos)
            if eat_pos:
                eats.append(eat(board, pos, eat_pos))
        yield from eats
        return
    for pos in board.fields_of(player):
        yield from possible_moves_for(board, pos)


'''
Alpha-beta pruning. See:
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
'''
def best_move(board, player, heuristic, la, musteat):
    best  = None
    a = float('-inf')
    b  = float('inf')
    for move in possible_moves(board, player, musteat):
        score = min_score(move, -player, musteat, heuristic, la - 1, a, b)
        if score > a:
            a = score
            best = move
    return best

def max_score(board, player, musteat, heuristic, la, a, b):
    if board.is_winner(player):
        return float('inf')
    if la <= 0:
        return heuristic(board)

    value = float('-inf')
    for move in possible_moves(board, player, musteat):
        score = min_score(move, -player, musteat, heuristic, la - 1, a, b)
        value = max(value, score)
        if value >= b:
            return value
        a = max(a, value)
    return value

def min_score(board, player, musteat, heuristic, la, a, b):
    if board.is_winner(player):
        return float('-inf')
    if la <= 0:
        return heuristic(board)

    value = float('inf')
    for move in possible_moves(board, player, musteat):
        score = max_score(move, -player, musteat, heuristic, la - 1, a, b)
        value = min(value, score)
        if value <= a:
            return value
        b = min(value, b)
    return value