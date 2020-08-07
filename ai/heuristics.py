from common.entities import Board, Player


def value_weighted(board, player):
    '''
    Only the number of each players' pieces is counted, with promoted pieces
    weighted additionally. Good enough for simple games, but ignores strategic
    positioning thus making it unsuitable for anything serious.
    '''
    basic_val, promoted_val = 1, 2

    def calc_score(player):
        score = 0
        for field in board.state:
            piece = field.piece
            if piece.player == player:
                score += promoted_val if piece.is_promoted else basic_val
        return score

    return calc_score(player) - calc_score(-player)


def value_and_position_weighted(board, player):
    '''
    Similar to value weighting, with additional value placed on unpromoted
    pieces closer to the opponent's end of the board, thus incentivizing
    aggressive play.
    '''
    basic_val, promoted_val = 2, 5
    coeff = .3

    def calc_score(player):
        score = 0
        for i, j in board.fields_of(player):
            piece = board[i, j].piece
            score += promoted_val if piece.is_promoted else basic_val
            if not piece.is_promoted:
                bonus = 0
                if player == Player.W and i >= Board.width//2:
                    bonus = coeff * i
                elif player == Player.B and i < Board.width//2:
                    bonus = coeff * (Board.width - i)
                score += bonus
        return score

    return calc_score(player) - calc_score(-player)
