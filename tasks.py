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


def get_capture_moves(piece, position):
    pass


class Board(object):

    def __init__(self, piece, position, place_enemies=False):
        self.piece = piece
        self.position = position
        self.setup_pieces(place_enemies)

    def setup_pieces(self, place_enemies):
        col, row = from_algebraic(self.position)

        squares = [[EMPTY for _ in range(8)] for _ in range(8)]
        squares[col][row] = FRIENDLY

        if place_enemies:
            enemies = 8
            while enemies:
                x, y = randrange(8), randrange(8)
                if not squares[x][y]:
                    squares[x][y] = ENEMY
                    enemies -= 1
        self.squares = squares

    def get_available_moves(self):
        col, row = from_algebraic(self.position)
        moves = []
        if self.piece == PAWN:
            moves = self.get_pawn_moves(col, row)
        elif self.piece == ROOK:
            moves = self.get_rook_moves(col, row)
        elif self.piece == BISHOP:
            moves = self.get_bishop_moves(col, row)
        elif self.piece == QUEEN:
            moves = self.get_queen_moves(col, row)
        elif self.piece == KING:
            moves = self.get_king_moves(col, row)
        elif self.piece == KNIGHT:
            moves = self.get_knight_moves(col, row)

        for idx, move in enumerate(moves):
            moves[idx] = to_algebraic(*move)
        return moves or 'No moves are available.'

    # Primitives for moving one square in a given direction
    def make_move(self, col, row, direction):
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

    # moves for specific pieces
    def get_pawn_moves(self, col, row):
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

    def get_rook_moves(self, col, row):
        all_moves = []
        for direction in [UP, RIGHT, DOWN, LEFT]:
            moves = [move for move in Moves(self, col, row, direction)]
            all_moves.extend(moves)
        return all_moves

    def get_bishop_moves(self, col, row):
        all_moves = []
        for direction in [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]:
            moves = [move for move in Moves(self, col, row, direction)]
            all_moves.extend(moves)
        return all_moves

    def get_queen_moves(self, col, row):
        return self.get_rook_moves(col, row) + self.get_bishop_moves(col, row)

    def get_king_moves(self, col, row):
        all_moves = []
        for direction in [UP, UP_RIGHT, RIGHT, DOWN_RIGHT,
                          DOWN, DOWN_LEFT, LEFT, UP_LEFT]:
            moves = [move for move in Moves(self, col, row, direction, 1)]
            all_moves.extend(moves)
        return all_moves

    def do_knight_move(self, col, row, first_move, second_move):
        try:
            new_col, new_row = first_move(col, row)
            new_col, new_row = first_move(new_col, new_row)
            return second_move(new_col, new_row)
        except NoMoveError:
            return None

    def get_knight_moves(self, col, row):
        moves = []
        moves.append(self.do_knight_move(col, row, move_up, move_left))
        moves.append(self.do_knight_move(col, row, move_up, move_right))
        moves.append(self.do_knight_move(col, row, move_down, move_left))
        moves.append(self.do_knight_move(col, row, move_down, move_right))
        moves.append(self.do_knight_move(col, row, move_left, move_up))
        moves.append(self.do_knight_move(col, row, move_left, move_down))
        moves.append(self.do_knight_move(col, row, move_right, move_up))
        moves.append(self.do_knight_move(col, row, move_right, move_down))

        return [move for move in moves if move]

    def __repr__(self):
        # print the board out for debug purposes
        # cols forward, rows backwards
        piece = 'N'
        board = ['\n']
        if self.piece != 'KNIGHT':
            piece = self.piece[0]
        for r in reversed(range(8)):
            for c in range(8):
                square = self.squares[c][r]
                if square == FRIENDLY:
                    board.append('[{}]'.format(piece))
                elif square == ENEMY:
                    board.append('[x]')
                else:
                    board.append('[ ]')
                    #  print '[{},{}]'.format(c, r),
            board.append('\n')
        return ''.join(board)


class Moves(object):

    def __init__(self, board, col, row, direction, limit=8):
        self.board = board
        self.col = col
        self.row = row
        self.direction = direction
        self.limit = limit
        self.num_returned = 0

    def next(self):
        if self.num_returned >= self.limit:
            raise StopIteration
        try:
            move = self.board.make_move(self.col, self.row, self.direction)
            self.col, self.row = move
            self.num_returned += 1
        except NoMoveError:
            raise StopIteration

        return move

    def __iter__(self):
        return self


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
        board = Board(args.piece, args.position)
        print board.get_available_moves()
