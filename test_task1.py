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

    def test_make_move_up(self):

        move = task1.make_move(0, 0, task1.UP)

        expected = 1, 0
        self.assertEqual(move, expected)
