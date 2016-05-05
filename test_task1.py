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


class TestTask1(unittest.TestCase):

    def test_make_move_up_a1(self):

        move = task1.make_move(0, 0, task1.UP)

        expected = 1, 0
        self.assertEqual(move, expected)

    def test_move_up_h1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 7, 0, task1.UP)

    def test_make_move_down_h1(self):

        move = task1.make_move(7, 0, task1.DOWN)

        expected = 6, 0
        self.assertEqual(move, expected)

    def test_move_down_a1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 0, 0, task1.DOWN)

    def test_move_left_a8(self):

        move = task1.make_move(0, 7, task1.LEFT)

        expected = 0, 6
        self.assertEqual(move, expected)

    def test_move_left_a1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 0, 0, task1.LEFT)

    def test_move_right_a8(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 0, 7, task1.RIGHT)

    def test_move_right_a1(self):

        move = task1.make_move(0, 0, task1.RIGHT)

        expected = 0, 1
        self.assertEqual(move, expected)

    def test_make_move_up_right_a1(self):

        move = task1.make_move(0, 0, task1.UP_RIGHT)

        expected = 1, 1
        self.assertEqual(move, expected)

    def test_move_up_right_h7(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 7, 6, task1.UP_RIGHT)

    def test_move_up_right_g8(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 6, 7, task1.UP_RIGHT)

    def test_make_move_down_right_h1(self):

        move = task1.make_move(7, 0, task1.DOWN_RIGHT)

        expected = 6, 1
        self.assertEqual(move, expected)

    def test_move_down_right_a7(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 0, 6, task1.DOWN_RIGHT)

    def test_move_down_right_b8(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 1, 7, task1.DOWN_RIGHT)

    def test_make_move_down_left_h8(self):

        move = task1.make_move(7, 7, task1.DOWN_LEFT)

        expected = 6, 6
        self.assertEqual(move, expected)

    def test_move_down_left_b1(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 1, 0, task1.DOWN_LEFT)

    def test_move_down_left_a2(self):

        expected = task1.NoMoveError
        self.assertRaises(expected, task1.make_move, 0, 1, task1.DOWN_LEFT)
