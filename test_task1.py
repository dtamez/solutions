#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Danny Tamez <zematynnad@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Tests for task1.py
"""
from __future__ import absolute_import

import unittest

import task1

# some constants to make the board positions easier to read
A, B, C, D, E, F, G, H = range(8)
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT = range(8)


class TestTask1(unittest.TestCase):

    def test_make_move_up_a1(self):

        move = task1.make_move(A, ONE, task1.UP)

        expected = A, TWO
        self.assertEqual(move, expected)

    def test_move_up_a8(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, A, EIGHT, task1.UP)

    def test_make_move_down_a8(self):

        move = task1.make_move(A, EIGHT, task1.DOWN)

        expected = A, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_a1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, A, ONE, task1.DOWN)

    def test_move_left_h1(self):

        move = task1.make_move(H, ONE, task1.LEFT)

        expected = G, ONE
        self.assertEqual(move, expected)

    def test_move_left_a1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, A, ONE, task1.LEFT)

    def test_move_right_h1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, H, ONE, task1.RIGHT)

    def test_move_right_a1(self):

        move = task1.make_move(A, ONE, task1.RIGHT)

        expected = B, ONE
        self.assertEqual(move, expected)

    def test_make_move_up_right_a1(self):

        move = task1.make_move(A, ONE, task1.UP_RIGHT)

        expected = B, TWO
        self.assertEqual(move, expected)

    def test_move_up_right_h7(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, H, SEVEN, task1.UP_RIGHT)

    def test_move_up_right_g8(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, G, EIGHT, task1.UP_RIGHT)

    def test_make_move_down_right_a8(self):

        move = task1.make_move(A, EIGHT, task1.DOWN_RIGHT)

        expected = B, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_right_g1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, G, ONE,
                          task1.DOWN_RIGHT)

    def test_move_down_right_h2(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, H, TWO,
                          task1.DOWN_RIGHT)

    def test_make_move_down_left_h8(self):

        move = task1.make_move(H, EIGHT, task1.DOWN_LEFT)

        expected = G, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_left_b1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, B, ONE, task1.DOWN_LEFT)

    def test_move_down_left_a2(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, A, TWO, task1.DOWN_LEFT)

    def test_make_move_up_left_h1(self):

        move = task1.make_move(H, ONE, task1.UP_LEFT)

        expected = G, TWO
        self.assertEqual(move, expected)

    def test_move_up_left_b8(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, B, EIGHT, task1.UP_LEFT)

    def test_move_up_left_a7(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, A, SEVEN, task1.UP_LEFT)

    def test_from_algebraic_a1(self):
        col, row = task1.from_algebraic('a1')

        expected = A, ONE
        self.assertTupleEqual((col, row), expected)

    def test_to_algebraic_0_0(self):
        position = task1.to_algebraic(0, 0)

        expected = 'a1'
        self.assertEqual(position, expected)

    def test_get_pawn_moves_a2(self):

        moves = task1.get_available_moves(task1.PAWN, 'a2')

        expected = ['a3', 'a4']
        self.assertListEqual(moves, expected)

    def test_get_pawn_moves_a1(self):

        expected = task1.IllegalPositionError
        self.assertRaises(expected, task1.get_available_moves,
                          task1.PAWN, 'a1')

    def test_get_pawn_moves_a8(self):

        moves = task1.get_available_moves(task1.PAWN, 'a8')

        expected = 'No moves are available.'
        self.assertEqual(moves, expected)

    def test_get_rook_moves(self):
        moves = task1.get_available_moves(task1.ROOK, 'a1')

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.assertListEqual(moves, expected)

    def test_get_rook_moves_e4(self):
        moves = task1.get_available_moves(task1.ROOK, 'e4')

        expected = ['e1', 'e2', 'e3', 'e5', 'e6', 'e7', 'e8',
                    'a4', 'b4', 'c4', 'd4', 'f4', 'g4', 'h4']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_a1(self):
        moves = task1.get_available_moves(task1.BISHOP, 'a1')

        expected = ['b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_e4(self):
        moves = task1.get_available_moves(task1.BISHOP, 'e4')

        expected = ['f5', 'g6', 'h7', 'd3', 'c2', 'b1', 'd5',
                    'c6', 'b7', 'a8', 'f3', 'g2', 'h1']
        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_a1(self):
        moves = task1.get_available_moves(task1.QUEEN, 'a1')

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                    'b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']

        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_e4(self):
        moves = task1.get_available_moves(task1.QUEEN, 'e4')

        expected = ['e1', 'e2', 'e3', 'e5', 'e6', 'e7', 'e8',
                    'a4', 'b4', 'c4', 'd4', 'f4', 'g4', 'h4',
                    'f5', 'g6', 'h7', 'd3', 'c2', 'b1', 'd5',
                    'c6', 'b7', 'a8', 'f3', 'g2', 'h1']

        self.assertItemsEqual(moves, expected)

    def test_get_king_moves_a1(self):
        moves = task1.get_available_moves(task1.KING, 'a1')

        expected = ['a2', 'b2', 'b1']

        self.assertItemsEqual(moves, expected)

    def test_get_king_moves_e4(self):
        moves = task1.get_available_moves(task1.KING, 'e4')

        expected = ['d3', 'd4', 'd5', 'e5', 'f5', 'f4', 'f3', 'e3']

        self.assertItemsEqual(moves, expected)
