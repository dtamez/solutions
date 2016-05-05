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

from task1 import get_available_moves


class TestTask1(unittest.TestCase):

    def test_get_available_moves_rook_a1(self):

        moves = get_available_moves('rook', 'a1')

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.assertItemsEqual(moves, expected)
