#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Chess game """

import time


class ChessPiece(object):
    """
    Class representing a chess piece
    """

    prefix = ''

    def __init__(self, position):
        """
        Constructor
        Args:
            position (String): Initial chess piece position
        Attributes:
            prefix (String): Class attribute - The chess piece's prefix
            position: Position of instance
        """

        position = str(position).strip().lower()
        self.moves = []
        self.position = position
        if not self.is_legal_move(position):
            excep = '`{}` is not a legal start position'
            raise ValueError(excep.format(position))

    def algebraic_to_numeric(self, tile):
        """
        Maps a valid algebraic expression to a tuple
        Args:
            position (String): Algebraic expression
        Returns:
            Mixed: Returns a tuple or False
        """
        keys = [x + str(y) for x in 'abcdefgh' for y in range(1, 9)]
        values = [(x, y) for x in xrange(8) for y in xrange(8)]
        boardmap = dict(zip(keys, values))

        tile = str(tile).strip().lower()
        if tile in boardmap.keys():
            return boardmap[tile]
        return False

    def is_legal_move(self, position):
        """
        Tests if position is on the chessboard.
        Args:
            position (String): Suggested position to test
        Returns:
            Boolean: True if position is legal, False otherwise
        """
        return isinstance(self.algebraic_to_numeric(position), tuple)

    def move(self, position):
        """
        Move chess piece
        Args:
            position (String): Algebraic expression.
        """
        if self.is_legal_move(position) and position != self.position:
            self.moves.append((self.prefix + self.position,
                               self.prefix + position,
                               time.time()))
            self.position = position
            return self.moves
        return False


class Rook(ChessPiece):
    """ Rook chess piece. """

    prefix = 'R'

    def is_legal_move(self, position):
        """
        Verifies Rook move is legal
        Args:
            position (String): Position to test
        Returns:
            Boolean: True if move is ok, else False.
        """
        mypos = self.algebraic_to_numeric(self.position)
        test = self.algebraic_to_numeric(position)
        return (mypos[0] == test[0] and mypos[1] != test[1]) or \
               (mypos[0] != test[0] and mypos[1] == test[1]) or \
               (mypos == test)


class Knight(ChessPiece):
    """ Knight chess piece """
    prefix = 'N'

    def is_legal_move(self, position):
        """
        Verifies Knight move is legal
        Args:
            position (String): Position to test
        Returns:
            Boolean: True if move is ok, else False.
        """
        my_piece = self.algebraic_to_numeric(self.position)
        test = self.algebraic_to_numeric(position)
        return test in [(my_piece[0] + 1, my_piece[1] + 3),
                        (my_piece[0] + 1, my_piece[1] - 3),
                        (my_piece[0] -1, my_piece[1] + 3),
                        (my_piece[0] - 1, my_piece[1] - 3),
                        (my_piece[0] + 3, my_piece[1] + 1),
                        (my_piece[0] + 3, my_piece[1] - 1),
                        (my_piece[0] - 3, my_piece[1] + 1),
                        (my_piece[0] - 3, my_piece[1] - 1), my_piece]


class Bishop(ChessPiece):
    """ Bishop chess piece """

    prefix = 'B'

    def is_legal_move(self, position):
        """
        Verifies Bishop move is legal
        Args:
        position (String): Position to test
        Returns:
            Boolean: True if move is ok, else False
        """

        mypos = self.algebraic_to_numeric(self.position)
        test = self.algebraic_to_numeric(position)
        d_mypos = min(mypos, test)
        d_test = max(mypos, test)
        return (mypos[0] + mypos[1] == test[0] + test[1]) or \
               (d_test[0] == abs(d_test[1]) - d_mypos[1]) or \
               (mypos == test)


class King(ChessPiece):
    """ King Chess Piece """

    prefix = 'K'

    def is_legal_move(self, position):
        """
        Verifies King move is legal
        Args:
            position (String): Position to test
        Returns:
            Boolean: True if move ok, else False
        """

        mypos = self.algebraic_to_numeric(self.position)
        test = self.algebraic_to_numeric(position)
        return (test in [(x, y) for x in range(mypos[0] - 1, mypos[0] + 2)
                         for y in range(mypos[1] - 1, mypos[1] + 2)])


class ChessMatch(object):
    """ Chess game """

    def __init__(self, pieces=None):
        """
        Constructor

        Args:
            pieces (dict): Dictionary of initial pieces positions
        """

        self.log = []

        if isinstance(pieces, dict):
            self.pieces = pieces
        else:
            self.reset()

    def __len__(self):
        """
        Return the number of log items
        Args:
            self: This object
        Returns:
            Int: Log length
        """
        return len(self.log)

    def reset(self):
        """
        Resets the match log to an empty list and
        places our pieces back at their starting
        positions.
        Args:
            self: This object
        Returns:
            None
        """

        positions = ['Ra1', 'Rh1', 'Ra8',
                     'Rh8', 'Bc1', 'Bf1',
                     'Bc8', 'Bf8', 'Ke1', 'Ke8']

        my_pieces = [Rook('a1'),
                     Rook('h1'),
                     Rook('a8'),
                     Rook('h8'),
                     Bishop('c1'),
                     Bishop('f1'),
                     Bishop('c8'),
                     Bishop('f8'),
                     King('e1'),
                     King('e8')]

        self.pieces = dict(zip(positions, my_pieces))
        self.log = []
        return None

    def move(self, piece, position):
        """
        Move a chess piece to a new position
        Args:
            piece (String): The name of the piece in Full Notation
            position (String): The destination coordinate in short notation
        Returns:
            Boolean: True if successful, false otherwise
        """

        if self.pieces[piece].move(position):
            my_piece = self.pieces[piece]
            my_move = my_piece.moves[-1]
            new_fn = my_move[1]
            self.pieces.pop(piece)
            self.pieces[new_fn] = my_piece
            self.log.append(my_move)
            return True
        return False


if __name__ == '__main__':
    import random

    MYPIECES = [Rook('d1'),
                Bishop('e3'),
                King('b5'),
                Knight('e5')]

    def chtest(piece):
        """
        Test suite for Chess pieces
        Args:
            piece(ChessPiece): Chess piece object
        Returns:
            (String): String output of positions
        """

        moves = [x + str(y) for x in 'abcdefgh' for y in range(1, 9)]
        ordered = moves[:]
        random.shuffle(moves)

        out = ''
        ptype = {'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'K': 'King'}

        print '### Random Test: ' + ptype[piece.prefix] + ' ###'

        for i in xrange(64):
            initial = piece.prefix + piece.position
            pos = moves[i]
            if piece.move(pos):
                out += 'Move {}: {} => {} succeeded.\n'.format(i,
                                                   initial,
                                                   piece.prefix + pos)

            else:
                out += 'Move {}: {} => {} failed.\n'.format(i,
                                                         initial,
                                                         piece.prefix + pos)

        return out

    for chpiece in MYPIECES:
        print chtest(chpiece)