#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Danny Tamez <zematynnad@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Algorithm for returning a list of moves (defined in algebraic notation) given
a starting square and a piece type.  It is assumed that the piece is a white
colored piece, so that for example, pawns would move from a2 to b2.
"""
from __future__ import absolute_import

import argparse

UP, RIGHT, LEFT, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, DOWN_RIGHT = range(8)
ROWS = {n: l for n, l in zip(range(8), list('abcdefgh'))}


class NoMoveError(Exception):
    pass


def make_move(row, col, direction):
    if direction == UP:
        return move_up(row,  col)
    else:
        pass


def move_up(row, col):
    if row == 7:
        raise NoMoveError()
    else:
        return row + 1, col


def get_available_moves(piece, position):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--piece', help='name of chess piece to move',
                        type=str)
    parser.add_argument('--position', help='starting point for piece',
                        type=str)
    args = parser.parse_args()
    get_available_moves(args.piece, args.position)
