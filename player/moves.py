from itertools import product

from common.eating import can_eat, eat
from common.entities import Player, Ver, Hor, Field, Board


def get_piece(board, player, musteat):
    pair = input().split()
    if len(pair) != 2:
        raise ValueError('Wait a second... Those are not integers!')
    
    i, j = int(pair[0]), int(pair[1])
    if not board[i, j].piece or board[i, j].piece.player != player:
        raise ValueError('Hey! That\'s not yours!')

    if musteat:
        can_i_eat = False
        for pos in board.fields_of(player):
            if can_eat(board, pos):
                can_i_eat = True
                break

        if can_i_eat and not can_eat(board, (i, j)):
            raise ValueError('Hey! You must eat!')

    return i, j


def get_move(board, player, pos, musteat):
    pair = input().split()
    if len(pair) != 2:
        raise ValueError('Wait a second... Those are not integers!')

    i, j = int(pair[0]), int(pair[1])
    move_to = board[i, j].piece
    piece   = board[pos].piece

    if move_to:
        raise ValueError('You can\'t move there.')
    
    off = i - pos[0], j - pos[1]

    # this is a mess; probably should get refactored to something sensible
    # for now, let's leave it as is
    if piece.is_promoted:
        if abs(off[0]) == 2 and abs(off[1]) == 2:
            mid_pos = pos[0] + off[0]//2, pos[1] + off[1]//2
            if not board[mid_pos].piece or board[mid_pos].piece.player == player:
                raise ValueError('You can\'t move there.')

            if off not in product([2*Ver.UP, 2*Ver.DOWN], [2*Hor.LEFT, 2*Hor.RIGHT]):
                raise ValueError('You can\'t move there.')        
        else:
            if off not in product([Ver.UP, Ver.DOWN], [Hor.LEFT, Hor.RIGHT]):
                raise ValueError('You can\'t move there.')        
    else:
        if player == Player.W:
            if abs(off[0]) == 2 and abs(off[1]) == 2:
                mid_pos = pos[0] + off[0]//2, pos[1] + off[1]//2
                if not board[mid_pos].piece or board[mid_pos].piece.player == player:
                    raise ValueError('You can\'t move there.')

                if off not in [(2*Ver.DOWN, 2*Hor.LEFT), (2*Ver.DOWN, 2*Hor.RIGHT)]:
                    raise ValueError('You can\'t move there.')
            else:
                if off not in [(Ver.DOWN, Hor.LEFT), (Ver.DOWN, Hor.RIGHT)]:
                    raise ValueError('You can\'t move there.')
        else: # player == Player.B
            if abs(off[0]) == 2 and abs(off[1]) == 2:
                mid_pos = pos[0] + off[0]//2, pos[1] + off[1]//2
                if not board[mid_pos].piece or board[mid_pos].piece.player == player:
                    raise ValueError('You can\'t move there.')

                if off not in [(2*Ver.UP, 2*Hor.LEFT), (2*Ver.UP, 2*Hor.RIGHT)]:
                    raise ValueError('You can\'t move there.')
            if off not in [(Ver.UP, Hor.LEFT), (Ver.UP, Hor.RIGHT)]:
                raise ValueError('You can\'t move there.')

    if musteat:
        if can_eat(board, pos) and (abs(off[0]) != 2 or abs(off[1]) != 2):
            raise ValueError('You must eat!')

    return i, j

def move_player(board, player, p, np):
    new = board.copy()
    new[p], new[np] = new[np], new[p]
    mid_pos = p[0] + int((np[0] - p[0])/2), p[1] + int((np[1] - p[1])/2)
    new[mid_pos] = Field()
    new.update()
    return new
