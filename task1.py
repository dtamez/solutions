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

UP, RIGHT, LEFT, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = range(8)
COLS = {n: l for n, l in zip(range(8), list('abcdefgh'))}
COLS_REVERSE = {v: k for k, v in COLS.items()}
PAWN = 'PAWN'
ROOK = 'ROOK'
KNIGHT = 'KNIGHT'
BISHOP = 'BISHOP'
QUEEN = 'QUEEN'
KING = 'KING'


class NoMoveError(Exception):
    pass


class IllegalPositionError(Exception):
    pass


def make_move(col, row, direction):
    if direction == UP:
        return move_up(col, row)
    elif direction == DOWN:
        return move_down(col, row)
    elif direction == LEFT:
        return move_left(col, row)
    elif direction == RIGHT:
        return move_right(col, row)
    elif direction == UP_RIGHT:
        return move_up(*move_right(col, row))
    elif direction == DOWN_RIGHT:
        return move_down(*move_right(col, row))
    elif direction == DOWN_LEFT:
        return move_down(*move_left(col, row))
    elif direction == UP_LEFT:
        return move_up(*move_left(col, row))


def move_up(col, row):
    if row == 7:
        raise NoMoveError()
    else:
        return col, row + 1


def move_down(col, row):
    if row == 0:
        raise NoMoveError()
    else:
        return col, row - 1


def move_left(col, row):
    if col == 0:
        raise NoMoveError()
    else:
        return col - 1, row


def move_right(col, row):
    if col == 7:
        raise NoMoveError()
    else:
        return col + 1, row


def get_pawn_moves(col, row):
    if row == 0:
        msg = 'This is not a valid position for a pawn.'
        raise IllegalPositionError(msg)
    moves = []
    moves.append(move_up(col, row))
    if row == 1:
        moves.append(move_up(*moves[-1]))
    return moves


def from_algebraic(position):
    col = COLS_REVERSE[position[0]]
    row = int(position[1]) - 1
    return col, row


def to_algebraic(col, row):
    return '{}{}'.format(COLS[col], row + 1)


def get_available_moves(piece, position):
    col, row = from_algebraic(position)
    moves = []
    if piece == PAWN:
        moves = get_pawn_moves(col, row)

    for idx, move in enumerate(moves):
        moves[idx] = to_algebraic(*move)
    return moves


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--piece', help='name of chess piece to move',
                        type=str)
    parser.add_argument('--position', help='starting point for piece',
                        type=str)
    args = parser.parse_args()
    get_available_moves(args.piece, args.position)
