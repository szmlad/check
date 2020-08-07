from copy import deepcopy
from enum import IntEnum


class Player(IntEnum):
    '''
    Two players are represented as an enumeration, with 1 for White and -1 for
    Black, so that programatically switching between them is as easy as negating
    the current player. Additionally, negation has some nice properties such as
    -(-x) = x.
    '''
    W = -1
    B =  1


class Ver(IntEnum):
    UP   = -1
    DOWN =  1


class Hor(IntEnum):
    LEFT  = -1
    RIGHT =  1


class Piece:
    def __init__(self, player, is_promoted=False):
        self.player = player
        self.is_promoted = is_promoted

    def __str__(self):
        if self.is_promoted:
            return self.player.name
        else:
            return self.player.name.lower()


class Field:
    def __init__(self, piece=None):
        self.piece = piece

    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return '.'


class Board:
    '''
    Game state. Essentially a wrapper around an 8x8 = 64 element array, each
    containing information about the piece residing on the corresponding field,
    if any.
    '''
    width = 8
    empty = 8
    pieces = 12

    def __init__(self):
        self.whites = Board.pieces
        self.blacks = Board.pieces
        self.winner = None
        self.state  = []

        for _ in range(Board.pieces):
            self.state.append(Field(Piece(Player.W)))
        for _ in range(Board.empty):
            self.state.append(Field())
        for _ in range(Board.pieces):
            self.state.append(Field(Piece(Player.B)))

    def __getitem__(self, pos):
        i, j = pos[0], pos[1]
        if i >= Board.width or j >= Board.width or i < 0 or j < 0:
            raise ValueError(f'({i}, {j}) out of range.')
        if (i + j) % 2 == 1:
            raise ValueError(f'({i}, {j}) is not accessible.')
        
        return self.state[i*Board.width//2 + j//2]

    def __setitem__(self, pos, value):
        i, j = pos[0], pos[1]
        if i >= Board.width or j >= Board.width or i < 0 or j < 0:
            raise ValueError(f'({i}, {j}) out of range.')
        if (i + j) % 2 == 1:
            raise ValueError(f'({i}, {j}) is not accessible.')
        
        self.state[i*Board.width//2 + j//2] = value

    def __str__(self):
        view = '  ' + ' '.join(str(n) for n in range(Board.width)) + '\n'
        for row in range(0, len(self.state), Board.width//2):
            view += f'{2*row//Board.width} '
            
            for col in range(Board.width):
                if (2*row//Board.width + col) % 2 == 1:
                    view += '.'
                else:
                    view += str(self.state[row + col//2])
                view += ' '
            
            view += '\n'
        return view

    def belongs_to(self, field, player):
        return field.piece and field.piece.player == player

    def fields_of(self, player):
        for index, field in enumerate(self.state):
            if self.belongs_to(field, player):
                i = index // (Board.width//2)
                j = i % 2 + 2 * (index % (Board.width//2))
                yield i, j

    def is_winner(self, player):
        return self.winner == player

    def update(self):
        self.whites = len(list(self.fields_of(Player.W)))
        self.blacks = len(list(self.fields_of(Player.B)))

        if self.whites == 0:
            self.winner = Player.B
        if self.blacks == 0:
            self.winner = Player.W

        for index in range(Board.width//2):
            if self.belongs_to(self.state[index], Player.B):
                self.state[index].piece.is_promoted = True

        for index in range(len(self.state) - Board.width//2, len(self.state)):
            if self.belongs_to(self.state[index], Player.W):
                self.state[index].piece.is_promoted = True

    def copy(self):
        new = Board()
        new.whites = self.whites
        new.blacks = self.blacks
        new.state  = deepcopy(self.state)
        return new
