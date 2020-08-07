from itertools import product

from common.entities import Player, Field, Board, Hor, Ver


def can_eat(board, p):
    '''
    Determine if the piece about to move can eat the oppponent's piece.
    '''
    piece = board[p].piece
    player = piece.player

    # get the directions in which a piece can move
    # if the piece is promoted, it can move in any direction
    # if not, white pieces move down and black pieces move up
    offsets = []
    if piece.is_promoted:
        offsets = product([Ver.DOWN, Ver.UP], [Hor.LEFT, Hor.RIGHT])
    elif player == Player.W:
        offsets = [(Ver.DOWN, Hor.LEFT), (Ver.DOWN, Hor.RIGHT)]
    else: # player == Player.B
        offsets = [(Ver.UP, Hor.LEFT), (Ver.UP, Hor.RIGHT)]

    for off in offsets:
        try:
            # this block is wrapped in a try-catch block to avoid going off the
            # bounds of the boardsx
            ep = p[0] + off[0], p[1] + off[1]
            if board[ep].piece and board[ep].piece.player == -player:
                np = ep[0] + off[0], ep[1] + off[1]
                if not board[np].piece:
                    return np
        except ValueError:
            continue

    return None


def eat(board, p, np):
    '''
    Eat the opponent's piece.
    '''
    new_state = board.copy()
    new_state[p], new_state[np] = new_state[np], new_state[p]
    enemy_pos = p[0] + (np[0] - p[0])//2, p[1] + (np[1] - p[1])//2
    new_state[enemy_pos] = Field()
    new_state.update()
    return new_state