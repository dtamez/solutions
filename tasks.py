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
from random import randrange

# Some constants to avoid typos, and make the code easier to read
# COLS and COLS_REVERSE are for switcing between indices and algebraic columns
UP, RIGHT, LEFT, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = range(8)
COLS = {n: l for n, l in zip(range(8), list('abcdefgh'))}
COLS_REVERSE = {v: k for k, v in COLS.items()}
PAWN = 'PAWN'
ROOK = 'ROOK'
KNIGHT = 'KNIGHT'
BISHOP = 'BISHOP'
QUEEN = 'QUEEN'
KING = 'KING'

EMPTY, FRIENDLY, ENEMY = range(3)


class NoMoveError(Exception):
    pass


class IllegalPositionError(Exception):
    pass


def get_available_moves(piece, position):
    col, row = from_algebraic(position)
    moves = []
    if piece == PAWN:
        moves = get_pawn_moves(col, row)
    elif piece == ROOK:
        moves = get_rook_moves(col, row)
    elif piece == BISHOP:
        moves = get_bishop_moves(col, row)
    elif piece == QUEEN:
        moves = get_queen_moves(col, row)
    elif piece == KING:
        moves = get_king_moves(col, row)
    elif piece == KNIGHT:
        moves = get_knight_moves(col, row)

    for idx, move in enumerate(moves):
        moves[idx] = to_algebraic(*move)
    return moves or 'No moves are available.'


def get_capture_moves(piece, position):
    pass


class Moves(object):

    def __init__(self, col, row, direction, limit=8):
        self.col = col
        self.row = row
        self.direction = direction
        self.limit = limit
        self.num_returned = 0

    def next(self):
        if self.num_returned >= self.limit:
            raise StopIteration
        try:
            move = make_move(self.col, self.row, self.direction)
            self.col, self.row = move
            self.num_returned += 1
        except NoMoveError:
            raise StopIteration

        return move

    def __iter__(self):
        return self


# Primitives for moving one square in a given direction
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


# moves for specific pieces
def get_pawn_moves(col, row):
    if row == 0:
        msg = 'This is not a valid position for a pawn.'
        raise IllegalPositionError(msg)
    moves = []
    try:
        moves.append(move_up(col, row))
    except NoMoveError:
        return moves

    if row == 1:
        moves.append(move_up(*moves[-1]))
    return moves


def get_rook_moves(col, row):
    all_moves = []
    for direction in [UP, RIGHT, DOWN, LEFT]:
        moves = [move for move in Moves(col, row, direction)]
        all_moves.extend(moves)
    return all_moves


def get_bishop_moves(col, row):
    all_moves = []
    for direction in [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]:
        moves = [move for move in Moves(col, row, direction)]
        all_moves.extend(moves)
    return all_moves


def get_queen_moves(col, row):
    return get_rook_moves(col, row) + get_bishop_moves(col, row)


def get_king_moves(col, row):
    all_moves = []
    for direction in [UP, UP_RIGHT, RIGHT, DOWN_RIGHT,
                      DOWN, DOWN_LEFT, LEFT, UP_LEFT]:
        moves = [move for move in Moves(col, row, direction, 1)]
        all_moves.extend(moves)
    return all_moves


def do_knight_move(col, row, first_move, second_move):
    try:
        new_col, new_row = first_move(col, row)
        new_col, new_row = first_move(new_col, new_row)
        return second_move(new_col, new_row)
    except NoMoveError:
        return None


def get_knight_moves(col, row):
    moves = []
    moves.append(do_knight_move(col, row, move_up, move_left))
    moves.append(do_knight_move(col, row, move_up, move_right))
    moves.append(do_knight_move(col, row, move_down, move_left))
    moves.append(do_knight_move(col, row, move_down, move_right))
    moves.append(do_knight_move(col, row, move_left, move_up))
    moves.append(do_knight_move(col, row, move_left, move_down))
    moves.append(do_knight_move(col, row, move_right, move_up))
    moves.append(do_knight_move(col, row, move_right, move_down))

    return [move for move in moves if move]


# helper functions for switching back and forth
# between algebraic notation and col, row format
def from_algebraic(position):
    col = COLS_REVERSE[position[0]]
    row = int(position[1]) - 1
    return col, row


def to_algebraic(col, row):
    return '{}{}'.format(COLS[col], row + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--piece', help='name of chess piece to move',
                        type=str)
    parser.add_argument('--position', help='starting point for piece',
                        type=str)
    parser.add_argument('--target',
                        help=('show minimum moves required to caputre '
                              'farthest enemy piece'), type=str)
    args = parser.parse_args()
    if args.target:
        print get_capture_moves(args.piece, args.position)
    else:
        print get_available_moves(args.piece, args.position)
