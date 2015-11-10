#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests Task 05."""


# Import Python libs
import unittest


# Import user libs
import chessmaster


class Task05TestCase(unittest.TestCase):
    """Task 05 tests"""

    def setUp(self):
        self.starting_positions = {
            'Ra1': chessmaster.Rook('a1'),
            'Rh1': chessmaster.Rook('h1'),
            'Ra8': chessmaster.Rook('a8'),
            'Rh8': chessmaster.Rook('h8'),
            'Bc1': chessmaster.Bishop('c1'),
            'Bf1': chessmaster.Bishop('f1'),
            'Bc8': chessmaster.Bishop('c8'),
            'Bf8': chessmaster.Bishop('f8'),
            'Ke1': chessmaster.King('e1'),
            'Ke8': chessmaster.King('e8'),
        }

    def get_start_positions(self, pieces):
        """Returns starting positions in a non-object dict."""
        {k: v.position for k, v in pieces.iteritems()}

    def test_starting_positions(self):
        """Tests the starting positions of the pieces after initialization."""
        cm = chessmaster.ChessMatch()
        cm_positions = self.get_start_positions(cm.pieces)
        st_positions = self.get_start_positions(self.starting_positions)
        self.assertEqual(cm_positions, st_positions)

    def test_constructor_pieces_param(self):
        """Tests the pieces parameter of the constructor."""
        pieces = {'Kd3': chessmaster.King('d3')}
        cm = chessmaster.ChessMatch(pieces)
        self.assertEqual(cm.pieces, pieces)

    def test_starting_log(self):
        """Tests the value of log at instantiation."""
        cm = chessmaster.ChessMatch()
        self.assertEqual(cm.log, [])

    def test_reset(self):
        """Tests the operation of the reset function."""
        cm = chessmaster.ChessMatch({'Kd3': chessmaster.King('d3')})
        cm.log = [('a', 'b')]
        cm.reset()
        self.assertEqual(cm.log, [])
        self.assertEqual(cm.pieces.keys(), self.starting_positions.keys())

    def test_move_log(self):
        """Tests that the move operation logs a move."""
        cm = chessmaster.ChessMatch()
        cm.move('Ke1', 'f2')
        cm.move('Ke8', 'd7')
        self.assertEqual(cm.log[0][:2], ('Ke1', 'Kf2'), 'Ke1 => f2')
        self.assertEqual(cm.log[1][:2], ('Ke8', 'Kd7'), 'Ke8 => d7')

    def test_move_pieces(self):
        """Tests that the move operation rekeys the object."""
        cm = chessmaster.ChessMatch()
        piece = cm.pieces['Ke1']
        cm.move('Ke1', 'f2')
        self.assertIs(cm.pieces['Kf2'], piece)
        self.assertNotIn('Ke1', cm.pieces)


if __name__ == '__main__':
    unittest.main()
