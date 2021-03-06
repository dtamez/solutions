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
import math
import sys
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


class NoPathToTargetError(Exception):
    pass


class IllegalPositionError(Exception):
    pass


class Board(object):

    def __init__(self, piece, position, place_enemies=False, show=False):
        self.piece = piece
        self.position = position
        self.col, self.row = from_algebraic(self.position)
        self.setup_pieces(place_enemies)
        self.targets = [(c, r) for c in range(8) for r in range(8)
                        if self.squares[c][r] == ENEMY]
        self.best = [0] * 100
        self.show = show
        if show:
            print self

    def setup_pieces(self, place_enemies):
        squares = [[EMPTY for _ in range(8)] for _ in range(8)]
        squares[self.col][self.row] = FRIENDLY

        if place_enemies:
            enemies = 8
            while enemies:
                x, y = randrange(8), randrange(8)
                if not squares[x][y]:
                    squares[x][y] = ENEMY
                    enemies -= 1
        self.squares = squares

    def get_available_moves(self):
        moves = self._get_available_moves(self.piece, self.col, self.row)
        for idx, move in enumerate(moves):
            moves[idx] = to_algebraic(*move)
        return moves or 'No moves are available.'

    def _get_available_moves(self, piece, col, row):
        moves = []
        if piece == PAWN:
            moves = self.get_pawn_moves(col, row)
        elif piece == ROOK:
            moves = self.get_rook_moves(col, row)
        elif piece == BISHOP:
            moves = self.get_bishop_moves(col, row)
        elif piece == QUEEN:
            moves = self.get_queen_moves(col, row)
        elif piece == KING:
            moves = self.get_king_moves(col, row)
        elif piece == KNIGHT:
            moves = self.get_knight_moves(col, row)

        return moves

    # Primitives for moving one square in a given direction
    def make_move(self, col, row, direction):
        if direction == UP:
            return self.move_up(col, row)
        elif direction == DOWN:
            return self.move_down(col, row)
        elif direction == LEFT:
            return self.move_left(col, row)
        elif direction == RIGHT:
            return self.move_right(col, row)
        elif direction == UP_RIGHT:
            return self.move_up(*self.move_right(col, row))
        elif direction == DOWN_RIGHT:
            return self.move_down(*self.move_right(col, row))
        elif direction == DOWN_LEFT:
            return self.move_down(*self.move_left(col, row))
        elif direction == UP_LEFT:
            return self.move_up(*self.move_left(col, row))

    # moves for specific pieces
    def get_pawn_moves(self, col, row):
        if row == 0:
            msg = 'This is not a valid position for a pawn.'
            raise IllegalPositionError(msg)
        moves = []
        # since we move straight but capture diagonally need to peek
        # at squares first
        if row == 7:
            return moves
        if col < 7:
            if self.squares[col + 1][row + 1] == ENEMY:
                moves.append(self.move_right(*self.move_up(col, row)))
        if col > 0:
            if self.squares[col - 1][row + 1] == ENEMY:
                moves.append(self.move_left(*self.move_up(col, row)))

        if self.squares[col][row + 1] == EMPTY:
            moves.append(self.move_up(col, row))
        if row == 1:
            if self.squares[col][row + 2] == EMPTY:
                moves.append(self.move_up(*moves[-1]))
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
        moves.append(self.do_knight_move(
            col, row, self.move_up, self.move_left))
        moves.append(self.do_knight_move(
            col, row, self.move_up, self.move_right))
        moves.append(self.do_knight_move(
            col, row, self.move_down, self.move_left))
        moves.append(self.do_knight_move(
            col, row, self.move_down, self.move_right))
        moves.append(self.do_knight_move(
            col, row, self.move_left, self.move_up))
        moves.append(self.do_knight_move(
            col, row, self.move_left, self.move_down))
        moves.append(self.do_knight_move(
            col, row, self.move_right, self.move_up))
        moves.append(self.do_knight_move(
            col, row, self.move_right, self.move_down))

        return [move for move in moves if move]

    def move_up(self, col, row):
        if row == 7:
            raise NoMoveError()
        else:
            return col, row + 1

    def move_down(self, col, row):
        if row == 0:
            raise NoMoveError()
        else:
            return col, row - 1

    def move_left(self, col, row):
        if col == 0:
            raise NoMoveError()
        else:
            return col - 1, row

    def move_right(self, col, row):
        if col == 7:
            raise NoMoveError()
        else:
            return col + 1, row

    def get_bishop_targets(self, targets):
        origin_color = (self.col - self.row) % 2
        to_remove = []
        for target in targets:
            # same color?
            target_color = (target[0] - target[1]) % 2
            if target_color != origin_color:
                to_remove.append(target)
        for t in to_remove:
            targets.remove(t)
        return targets

    def get_pawn_targets(self, targets):
        enemies_this_col = [(self.col, r) for r in range(8)
                            if self.squares[self.col][r] == ENEMY]
        to_remove = []
        for target in targets:
            blocked = [e for e in enemies_this_col if e[1] < target[1]]
            wrong_column = abs(target[0] - self.col) != 1
            is_behind_pawn = target[1] <= self.row
            if blocked or wrong_column or is_behind_pawn:
                to_remove.append(target)
        for t in to_remove:
            targets.remove(t)
        return targets

    def get_farthest_target(self):
        targets = [(c, r) for c in range(8) for r in range(8)
                   if self.squares[c][r] == ENEMY]
        if self.piece == BISHOP:
            targets = self.get_bishop_targets(targets)
        elif self.piece == PAWN:
            targets = self.get_pawn_targets(targets)

        farthest = None
        farthest_target = None
        x1, y1 = self.col, self.row
        for x2, y2 in targets:
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist > farthest:
                farthest = dist
                farthest_target = x2, y2

        return farthest_target

    def get_fewest_moves_to_all_targets(self):
        # approximate solution
        steps = []
        remaining = self.targets[:]
        origin = (self.col, self.row)
        while remaining:
            self.best = [0] * 100
            moves = self.get_nearest_target(origin, remaining)
            steps.append(moves[1:])
            origin = moves.pop()
            # update our inner state
            self.squares[self.col][self.row] = EMPTY
            self.col, self.row = origin
            self.squares[self.col][self.row] = FRIENDLY
            if self.show:
                print self
            if remaining:
                remaining.remove(origin)

        total = sum([len(s) for s in steps]) - 1
        if self.show:
            print 'targets: {} '.format(
                [to_algebraic(*t) for t in self.targets])
            print '{} total steps to capture all targets'.format(total)
        return [[to_algebraic(*s) for s in step] for step in steps]

    def get_nearest_target(self, origin, targets):
        nearest = None
        for target in targets:
            moves = self.get_shortest_path(origin, target, [], {})
            if not moves:
                # this target may return no moves if a previous target
                # was a direct capture
                continue
            if not nearest or (moves and len(moves) < len(nearest)):
                nearest = moves[:]
        return nearest

    def get_fewest_moves_to_farthest_target(self):
        origin = self.col, self.row
        target = self.get_farthest_target()
        # may need to set up the targets again
        # if they are not valid for this piece
        while not target:
            self.setup_pieces(True)
            target = self.get_farthest_target()
        path = self.get_shortest_path(origin, target, [], {})

        if self.show:
            print '{} move{} from {} to {}'.format(
                len(path) - 1, '' if len(path) == 2 else 's',
                to_algebraic(*origin), to_algebraic(*target))
        return [to_algebraic(*p) for p in path if p]

    def get_shortest_path(self, origin, target, path, seen):
        path.append(origin)
        seen[origin] = len(path)
        avail = self._get_available_moves(self.piece, *origin)
        # is there a direct move available?
        if target in avail:
            # potential best solution
            path.append(target)
            if len(path) < len(self.best):
                self.best = path[:]
            path.pop()
            path.pop()
        elif avail:
            # go one level deeper
            if len(self.best) - len(path) == 1:
                path.pop()
                return
            for move in avail:
                if move in seen and seen[move] < len(path):
                    continue
                self.get_shortest_path(move, target, path, seen)
            path.pop()
        return self.best

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
        # if this space was captured stop iterating, however, if
        # after the capture we are looking for moves anew
        # (num_returned == 0) then don't stop the iteration as the
        # enemy is not really there in this case
        if (self.board.squares[self.col][self.row] == ENEMY and
                self.num_returned > 0):
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
                              'farthest enemy piece'), action='store_true')
    parser.add_argument('--collect',
                        help=('show minimum moves required to caputre '
                              'all enemy piece'), action='store_true')
    parser.add_argument('--show_board',
                        help=('show board positions' 'show_board'),
                        action='store_true')
    args = parser.parse_args()
    enemies = args.collect or args.target
    if args.collect and args.target:
        print 'Choose target or collect but not both.'
        sys.exit()
    if args.collect:
        if args.piece in [PAWN, BISHOP]:
            print ("{}s can't cover all squares, so they're not allowed"
                   " with the --collect option".format(args.piece))
            sys.exit()
    board = Board(args.piece, args.position, place_enemies=enemies,
                  show=args.show_board)
    if args.target:
        print board.get_fewest_moves_to_farthest_target()
    elif args.collect:
        print board.get_fewest_moves_to_all_targets()
    else:
        print board.get_available_moves()
