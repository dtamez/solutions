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
