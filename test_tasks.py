#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Danny Tamez <zematynnad@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Tests for tasks.py
"""
from __future__ import absolute_import

import unittest

import tasks

# some constants to make the board positions easier to read
A, B, C, D, E, F, G, H = range(8)
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT = range(8)


class Testtasks(unittest.TestCase):

    def test_make_move_up_a1(self):

        move = tasks.make_move(A, ONE, tasks.UP)

        expected = A, TWO
        self.assertEqual(move, expected)

    def test_move_up_a8(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, A, EIGHT, tasks.UP)

    def test_make_move_down_a8(self):

        move = tasks.make_move(A, EIGHT, tasks.DOWN)

        expected = A, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_a1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, A, ONE, tasks.DOWN)

    def test_move_left_h1(self):

        move = tasks.make_move(H, ONE, tasks.LEFT)

        expected = G, ONE
        self.assertEqual(move, expected)

    def test_move_left_a1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, A, ONE, tasks.LEFT)

    def test_move_right_h1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, H, ONE, tasks.RIGHT)

    def test_move_right_a1(self):

        move = tasks.make_move(A, ONE, tasks.RIGHT)

        expected = B, ONE
        self.assertEqual(move, expected)

    def test_make_move_up_right_a1(self):

        move = tasks.make_move(A, ONE, tasks.UP_RIGHT)

        expected = B, TWO
        self.assertEqual(move, expected)

    def test_move_up_right_h7(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, H, SEVEN, tasks.UP_RIGHT)

    def test_move_up_right_g8(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, G, EIGHT, tasks.UP_RIGHT)

    def test_make_move_down_right_a8(self):

        move = tasks.make_move(A, EIGHT, tasks.DOWN_RIGHT)

        expected = B, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_right_g1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, G, ONE,
                          tasks.DOWN_RIGHT)

    def test_move_down_right_h2(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, H, TWO,
                          tasks.DOWN_RIGHT)

    def test_make_move_down_left_h8(self):

        move = tasks.make_move(H, EIGHT, tasks.DOWN_LEFT)

        expected = G, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_left_b1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, B, ONE, tasks.DOWN_LEFT)

    def test_move_down_left_a2(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, A, TWO, tasks.DOWN_LEFT)

    def test_make_move_up_left_h1(self):

        move = tasks.make_move(H, ONE, tasks.UP_LEFT)

        expected = G, TWO
        self.assertEqual(move, expected)

    def test_move_up_left_b8(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, B, EIGHT, tasks.UP_LEFT)

    def test_move_up_left_a7(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, tasks.make_move, A, SEVEN, tasks.UP_LEFT)

    def test_from_algebraic_a1(self):
        col, row = tasks.from_algebraic('a1')

        expected = A, ONE
        self.assertTupleEqual((col, row), expected)

    def test_to_algebraic_0_0(self):
        position = tasks.to_algebraic(0, 0)

        expected = 'a1'
        self.assertEqual(position, expected)

    def test_get_pawn_moves_a2(self):

        moves = tasks.get_available_moves(tasks.PAWN, 'a2')

        expected = ['a3', 'a4']
        self.assertListEqual(moves, expected)

    def test_get_pawn_moves_a1(self):

        expected = tasks.IllegalPositionError
        self.assertRaises(expected, tasks.get_available_moves,
                          tasks.PAWN, 'a1')

    def test_get_pawn_moves_a8(self):

        moves = tasks.get_available_moves(tasks.PAWN, 'a8')

        expected = 'No moves are available.'
        self.assertEqual(moves, expected)

    def test_get_rook_moves(self):
        moves = tasks.get_available_moves(tasks.ROOK, 'a1')

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.assertListEqual(moves, expected)

    def test_get_rook_moves_e4(self):
        moves = tasks.get_available_moves(tasks.ROOK, 'e4')

        expected = ['e1', 'e2', 'e3', 'e5', 'e6', 'e7', 'e8',
                    'a4', 'b4', 'c4', 'd4', 'f4', 'g4', 'h4']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_a1(self):
        moves = tasks.get_available_moves(tasks.BISHOP, 'a1')

        expected = ['b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_e4(self):
        moves = tasks.get_available_moves(tasks.BISHOP, 'e4')

        expected = ['f5', 'g6', 'h7', 'd3', 'c2', 'b1', 'd5',
                    'c6', 'b7', 'a8', 'f3', 'g2', 'h1']
        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_a1(self):
        moves = tasks.get_available_moves(tasks.QUEEN, 'a1')

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                    'b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']

        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_e4(self):
        moves = tasks.get_available_moves(tasks.QUEEN, 'e4')

        expected = ['e1', 'e2', 'e3', 'e5', 'e6', 'e7', 'e8',
                    'a4', 'b4', 'c4', 'd4', 'f4', 'g4', 'h4',
                    'f5', 'g6', 'h7', 'd3', 'c2', 'b1', 'd5',
                    'c6', 'b7', 'a8', 'f3', 'g2', 'h1']

        self.assertItemsEqual(moves, expected)

    def test_get_king_moves_a1(self):
        moves = tasks.get_available_moves(tasks.KING, 'a1')

        expected = ['a2', 'b2', 'b1']

        self.assertItemsEqual(moves, expected)

    def test_get_king_moves_e4(self):
        moves = tasks.get_available_moves(tasks.KING, 'e4')

        expected = ['d3', 'd4', 'd5', 'e5', 'f5', 'f4', 'f3', 'e3']

        self.assertItemsEqual(moves, expected)

    def test_get_knight_moves_a1(self):
        moves = tasks.get_available_moves(tasks.KNIGHT, 'a1')

        expected = ['b3', 'c2']

        self.assertItemsEqual(moves, expected)

    def test_get_knight_moves_e4(self):
        moves = tasks.get_available_moves(tasks.KNIGHT, 'e4')

        expected = ['d6', 'f6', 'g5', 'g3', 'f2', 'd2', 'c3', 'c5']

        self.assertItemsEqual(moves, expected)

    def test_get_board(self):
        position = 'd3'
        col, row = tasks.from_algebraic('d3')

        board = tasks.Board(tasks.ROOK, position)

        self.assertEqual(board.squares[col][row], tasks.FRIENDLY)

    def test_random_enemies(self):
        position = 'd3'

        board = tasks.Board(tasks.ROOK, position)

        expected = 8
        actual = sum([row.count(tasks.ENEMY) for row in board.squares])
        self.assertEqual(actual, expected)
