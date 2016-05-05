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

    def test_get_pawn_moves_a2(self):

        move = task1.get_available_moves((task1.PAWN, 'a2'))

        expected = ['a3', 'a4']
        self.assertListEqual(move, expected)
