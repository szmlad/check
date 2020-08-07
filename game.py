from argparse import Action, ArgumentParser
from os import system
from time import time

from ai.heuristics import value_weighted, value_and_position_weighted
from ai.moves import best_move, possible_moves_for
from common.eating import can_eat, eat
from common.entities import Player, Board
from player.moves import get_piece, get_move, move_player


def parse_commandline_args():
    parser = ArgumentParser()
    parser.add_argument('-m', '--musteat', action='store_true')
    parser.add_argument('-l', '--lookahead', type=int, default=6)
    parser.add_argument('--heuristic')
    return parser.parse_args()


def parse_heuristic(heuristic_description):
    if heuristic_description == 'basic':
        return lambda board: value_weighted(board, Player.B)
    elif heuristic_description == 'advanced':
        return lambda board: value_and_position_weighted(board, Player.B)
    else:
        print(f'No heuristic called {heuristic_description}.')
        print('Falling back to basic...')
        return lambda board: value_weighted(board, Player.B)


def play_game():
    args = parse_commandline_args()

    board = Board()
    player = Player.W
    musteat = args.musteat
    lookahead = args.lookahead
    heuristic = parse_heuristic(args.heuristic)

    spent = None
    while True:
        if board.is_winner(-player):
            if -player == Player.B:
                print('Computer has won!')
            else:
                print('You have won! Wow!')
            return
        
        if player == Player.W:
            try:
                print(board)

                if spent:
                    print(f'Black was thinking for {spent} seconds.')

                print('Choose your piece. \n> ', end='')
                pos = get_piece(board, player, musteat)

                print('Choose where to move. \n> ', end='')
                new_pos = get_move(board, player, pos, musteat)

                board = move_player(board, player, pos, new_pos)
            except ValueError as e:
                print(e)
                continue
        else:
            start = time()
            board = best_move(board, player, heuristic, lookahead, musteat)
            end = time()
            spent = end - start

        player = -player


if __name__ == '__main__':
    play_game()