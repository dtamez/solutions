#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Danny Tamez <zematynnad@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Tests for tasks.py
"""
from __future__ import absolute_import

import unittest

import tasks

# some constants to make the board positions easier to read
A, B, C, D, E, F, G, H = range(8)
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT = range(8)


class TestMovesPrimitives(unittest.TestCase):

    def setUp(self):
        self.board = tasks.Board(tasks.KING, 'a1')

    def test_make_move_up_a1(self):

        move = self.board.make_move(A, ONE, tasks.UP)

        expected = A, TWO
        self.assertEqual(move, expected)

    def test_move_up_a8(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move, A, EIGHT, tasks.UP)

    def test_make_move_down_a8(self):

        move = self.board.make_move(A, EIGHT, tasks.DOWN)

        expected = A, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_a1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move, A, ONE, tasks.DOWN)

    def test_move_left_h1(self):

        move = self.board.make_move(H, ONE, tasks.LEFT)

        expected = G, ONE
        self.assertEqual(move, expected)

    def test_move_left_a1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move, A, ONE, tasks.LEFT)

    def test_move_right_h1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move, H, ONE, tasks.RIGHT)

    def test_move_right_a1(self):

        move = self.board.make_move(A, ONE, tasks.RIGHT)

        expected = B, ONE
        self.assertEqual(move, expected)

    def test_make_move_up_right_a1(self):

        move = self.board.make_move(A, ONE, tasks.UP_RIGHT)

        expected = B, TWO
        self.assertEqual(move, expected)

    def test_move_up_right_h7(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move,
                          H, SEVEN, tasks.UP_RIGHT)

    def test_move_up_right_g8(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move,
                          G, EIGHT, tasks.UP_RIGHT)

    def test_make_move_down_right_a8(self):

        move = self.board.make_move(A, EIGHT, tasks.DOWN_RIGHT)

        expected = B, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_right_g1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move, G, ONE,
                          tasks.DOWN_RIGHT)

    def test_move_down_right_h2(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move, H, TWO,
                          tasks.DOWN_RIGHT)

    def test_make_move_down_left_h8(self):

        move = self.board.make_move(H, EIGHT, tasks.DOWN_LEFT)

        expected = G, SEVEN
        self.assertEqual(move, expected)

    def test_move_down_left_b1(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move,
                          B, ONE, tasks.DOWN_LEFT)

    def test_move_down_left_a2(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move,
                          A, TWO, tasks.DOWN_LEFT)

    def test_make_move_up_left_h1(self):

        move = self.board.make_move(H, ONE, tasks.UP_LEFT)

        expected = G, TWO
        self.assertEqual(move, expected)

    def test_move_up_left_b8(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move,
                          B, EIGHT, tasks.UP_LEFT)

    def test_move_up_left_a7(self):

        expected = tasks.NoMoveError
        self.assertRaises(expected, self.board.make_move,
                          A, SEVEN, tasks.UP_LEFT)

    def test_from_algebraic_a1(self):
        col, row = tasks.from_algebraic('a1')

        expected = A, ONE
        self.assertTupleEqual((col, row), expected)

    def test_to_algebraic_0_0(self):
        position = tasks.to_algebraic(0, 0)

        expected = 'a1'
        self.assertEqual(position, expected)


class TestMovesNoEnemies(unittest.TestCase):
    def test_get_pawn_moves_a2(self):
        board = tasks.Board(tasks.PAWN, 'a2')

        moves = board.get_available_moves()

        expected = ['a3', 'a4']
        self.assertListEqual(moves, expected)

    def test_get_pawn_moves_a1(self):
        board = tasks.Board(tasks.PAWN, 'a1')

        expected = tasks.IllegalPositionError
        self.assertRaises(expected, board.get_available_moves)

    def test_get_pawn_moves_a8(self):
        board = tasks.Board(tasks.PAWN, 'a8')

        moves = board.get_available_moves()

        expected = 'No moves are available.'
        self.assertEqual(moves, expected)

    def test_get_rook_moves(self):
        board = tasks.Board(tasks.ROOK, 'a1')

        moves = board.get_available_moves()

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.assertListEqual(moves, expected)

    def test_get_rook_moves_e4(self):
        board = tasks.Board(tasks.ROOK, 'e4')

        moves = board.get_available_moves()

        expected = ['e1', 'e2', 'e3', 'e5', 'e6', 'e7', 'e8',
                    'a4', 'b4', 'c4', 'd4', 'f4', 'g4', 'h4']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_a1(self):
        board = tasks.Board(tasks.BISHOP, 'a1')

        moves = board.get_available_moves()

        expected = ['b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_e4(self):
        board = tasks.Board(tasks.BISHOP, 'e4')

        moves = board.get_available_moves()

        expected = ['f5', 'g6', 'h7', 'd3', 'c2', 'b1', 'd5',
                    'c6', 'b7', 'a8', 'f3', 'g2', 'h1']
        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_a1(self):
        board = tasks.Board(tasks.QUEEN, 'a1')

        moves = board.get_available_moves()

        expected = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                    'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                    'b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']
        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_e4(self):
        board = tasks.Board(tasks.QUEEN, 'e4')

        moves = board.get_available_moves()

        expected = ['e1', 'e2', 'e3', 'e5', 'e6', 'e7', 'e8',
                    'a4', 'b4', 'c4', 'd4', 'f4', 'g4', 'h4',
                    'f5', 'g6', 'h7', 'd3', 'c2', 'b1', 'd5',
                    'c6', 'b7', 'a8', 'f3', 'g2', 'h1']
        self.assertItemsEqual(moves, expected)

    def test_get_king_moves_a1(self):
        board = tasks.Board(tasks.KING, 'a1')

        moves = board.get_available_moves()

        expected = ['a2', 'b2', 'b1']
        self.assertItemsEqual(moves, expected)

    def test_get_king_moves_e4(self):
        board = tasks.Board(tasks.KING, 'e4')

        moves = board.get_available_moves()

        expected = ['d3', 'd4', 'd5', 'e5', 'f5', 'f4', 'f3', 'e3']
        self.assertItemsEqual(moves, expected)

    def test_get_knight_moves_a1(self):
        board = tasks.Board(tasks.KNIGHT, 'a1')

        moves = board.get_available_moves()

        expected = ['b3', 'c2']
        self.assertItemsEqual(moves, expected)

    def test_get_knight_moves_e4(self):
        board = tasks.Board(tasks.KNIGHT, 'e4')

        moves = board.get_available_moves()

        expected = ['d6', 'f6', 'g5', 'g3', 'f2', 'd2', 'c3', 'c5']
        self.assertItemsEqual(moves, expected)

    def test_get_board(self):
        position = 'd3'
        col, row = tasks.from_algebraic('d3')

        board = tasks.Board(tasks.ROOK, position)

        self.assertEqual(board.squares[col][row], tasks.FRIENDLY)


class TestMovesWithEnemies(unittest.TestCase):

    def test_random_enemies(self):

        board = tasks.Board(tasks.ROOK, 'd3', True)

        expected = 8
        actual = sum([row.count(tasks.ENEMY) for row in board.squares])
        self.assertEqual(actual, expected)

    def test_board_no_enemies(self):

        board = tasks.Board(tasks.ROOK, 'd3')

        expected = 0
        actual = sum([row.count(tasks.ENEMY) for row in board.squares])
        self.assertEqual(actual, expected)

    def get_custom_board(self, piece, position, *enemies):
        board = tasks.Board(piece, position)
        for enemy in enemies:
            col, row = tasks.from_algebraic(enemy)
            board.squares[col][row] = tasks.ENEMY
        return board

    def test_get_rook_moves_a1_enemy_at_a4(self):
        board = self.get_custom_board(tasks.ROOK, 'a1', 'a4')

        moves = board.get_available_moves()

        expected = ['a2', 'a3', 'a4', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        self.assertItemsEqual(moves, expected)

    def test_get_rook_moves_e4_4_enemies(self):
        board = self.get_custom_board(tasks.ROOK, 'e4', 'c4', 'e6', 'g4', 'e2')

        moves = board.get_available_moves()

        expected = ['e5', 'e6', 'f4', 'g4', 'e3', 'e2', 'd4', 'c4']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_a1_enemy_at_d4(self):
        board = self.get_custom_board(tasks.BISHOP, 'a1', 'd4')

        moves = board.get_available_moves()

        expected = ['b2', 'c3', 'd4']
        self.assertItemsEqual(moves, expected)

    def test_get_bishop_moves_e4_4_enemies(self):
        board = self.get_custom_board(tasks.BISHOP,
                                      'e4', 'd5', 'f5', 'f3', 'd3')

        moves = board.get_available_moves()

        expected = ['d5', 'f5', 'f3', 'd3']
        self.assertItemsEqual(moves, expected)

    def test_get_queen_moves_a1_captures_only(self):
        board = self.get_custom_board(tasks.QUEEN, 'a1', 'a2', 'b2', 'b1')

        moves = board.get_available_moves()

        expected = ['a2', 'b2', 'b1']
        self.assertItemsEqual(moves, expected)

    def test_knight_moves_a1_surrounded(self):
        board = self.get_custom_board(tasks.KNIGHT, 'a1', 'a2', 'b2', 'b1')

        moves = board.get_available_moves()

        expected = ['b3', 'c2']
        self.assertItemsEqual(moves, expected)

    def test_pawn_moves_a2_enemies_a4_b3(self):
        board = self.get_custom_board(tasks.PAWN, 'a2', 'a4', 'b3')

        moves = board.get_available_moves()

        expected = ['a3', 'b3']
        self.assertItemsEqual(moves, expected)

    def test_determine_farthest_enemy(self):
        targets = ['b2', 'a5', 'b5', 'c5', 'c4', 'c3', 'd3', 'e3', 'e4']
        board = self.get_custom_board(tasks.QUEEN, 'a1', *targets)

        farthest = board.get_farthest_target()

        expected = tasks.from_algebraic('e4')
        self.assertEqual(farthest, expected)

    def test_get_shortest_move_finds_direct_target(self):
        board = self.get_custom_board(tasks.ROOK, 'a1', 'c1')
        origin = tasks.from_algebraic('a1')
        target = tasks.from_algebraic('c1')

        path = board.get_shortest_path(origin, target, [], {})

        self.assertEqual(path, [origin, target])

    def test_get_shortest_path_finds_2_step_target(self):
        board = self.get_custom_board(tasks.ROOK, 'a1', 'c2')
        origin = tasks.from_algebraic('a1')
        target = tasks.from_algebraic('c2')

        path = board.get_shortest_path(origin, target, [], {})

        expected = [origin, tasks.from_algebraic('a2'), target]
        self.assertEqual(path, expected)

    def test_get_shortest_path_when_not_first_discovered(self):
        targets = ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
        board = self.get_custom_board(tasks.ROOK, 'a1', *targets)
        origin = tasks.from_algebraic('a1')
        target = tasks.from_algebraic('a8')

        path = board.get_shortest_path(origin, target, [], {})

        b1 = tasks.from_algebraic('b1')
        b8 = tasks.from_algebraic('b8')
        expected = [origin, b1, b8, target]
        self.assertEqual(path, expected)

    def test_get_shortest_path_to_target_queen(self):
        targets = ['b2', 'a5', 'b5', 'c5', 'c4', 'c3', 'd3', 'e3', 'e4']
        board = self.get_custom_board(tasks.QUEEN, 'a1', *targets)
        origin = tasks.from_algebraic('a1')
        target = tasks.from_algebraic('e4')

        moves = board.get_shortest_path(origin, target, [], {})

        h1 = tasks.from_algebraic('h1')
        expected = [origin, h1, target]
        self.assertEqual(moves, expected)

    def test_get_shortest_path_to_target_king(self):
        targets = ['a3', 'b3', 'c3', 'c2', 'c1', 'd3']
        board = self.get_custom_board(tasks.KING, 'a1', *targets)
        origin = tasks.from_algebraic('a1')
        target = tasks.from_algebraic('d3')

        moves = board.get_shortest_path(origin, target, [], {})

        b2 = tasks.from_algebraic('b2')
        c3 = tasks.from_algebraic('c3')
        expected = [origin, b2, c3, target]
        self.assertEqual(moves, expected)

    def test_get_shortest_path_to_target_knight(self):
        targets = ['a5', 'b5', 'c5', 'd5', 'd4', 'd3', 'd2', 'd1']
        board = self.get_custom_board(tasks.KNIGHT, 'a1', *targets)
        origin = tasks.from_algebraic('a1')
        target = tasks.from_algebraic('d5')

        moves = board.get_shortest_path(origin, target, [], {})

        c2 = tasks.from_algebraic('c2')
        b4 = tasks.from_algebraic('b4')
        expected = [origin, c2, b4, target]
        self.assertEqual(moves, expected)

    def test_get_shortest_path_to_target_bishop(self):
        targets = ['c6', 'g6', 'g2', 'c2', 'a6']
        board = self.get_custom_board(tasks.BISHOP, 'e4', *targets)
        origin = tasks.from_algebraic('e4')
        target = tasks.from_algebraic('a6')

        moves = board.get_shortest_path(origin, target, [], {})

        d3 = tasks.from_algebraic('d3')
        expected = [origin, d3, target]
        self.assertEqual(moves, expected)

    def test_get_shortest_path_to_target_pawns(self):
        targets = ['e4', 'f4', 'e5']
        board = self.get_custom_board(tasks.PAWN, 'e2', *targets)
        origin = tasks.from_algebraic('e2')
        target = tasks.from_algebraic('e5')

        moves = board.get_shortest_path(origin, target, [], {})

        e3 = tasks.from_algebraic('e3')
        f4 = tasks.from_algebraic('f4')
        expected = [origin, e3, f4, target]
        self.assertEqual(moves, expected)

    def test_get_fewest_moves_to_target_bishop_wrong_color(self):
        targets = ['c6', 'g6', 'g2', 'c2', 'a7', 'a6']
        board = self.get_custom_board(tasks.BISHOP, 'e4', *targets)

        moves = board.get_fewest_moves_to_farthest_target()

        expected = ['e4', 'd3', 'a6']
        self.assertEqual(moves, expected)

    def test_get_fewest_moves_to_target_bishop_no_target_works(self):
        targets = ['a7']
        board = self.get_custom_board(tasks.BISHOP, 'e4', *targets)

        moves = board.get_fewest_moves_to_farthest_target()

        new_targets = [(c, r) for c in range(8) for r in range(8)
                       if board.squares[c][r] == tasks.ENEMY]
        self.assertNotEqual(targets, new_targets)
        self.assertIsNotNone(moves)

    def test_get_fewest_moves_to_target_pawn_no_target_works(self):
        targets = ['a7']
        board = self.get_custom_board(tasks.PAWN, 'h2', *targets)

        moves = board.get_fewest_moves_to_farthest_target()

        new_targets = [(c, r) for c in range(8) for r in range(8)
                       if board.squares[c][r] == tasks.ENEMY]
        self.assertNotEqual(targets, new_targets)
        self.assertIsNotNone(moves)

    def test_get_fewest_moves_to_target_pawn_blocked(self):
        targets = ['h4', 'g5']
        board = self.get_custom_board(tasks.PAWN, 'h2', *targets)

        moves = board.get_fewest_moves_to_farthest_target()

        new_targets = [(c, r) for c in range(8) for r in range(8)
                       if board.squares[c][r] == tasks.ENEMY]
        self.assertNotEqual(targets, new_targets)
        self.assertIsNotNone(moves)

    def test_get_nearest_target_king(self):
        targets = ['g4', 'h5']
        board = self.get_custom_board(tasks.KING, 'h2', *targets)
        origin = tasks.from_algebraic('h2')
        targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_nearest_target(origin, targets)

        h3 = tasks.from_algebraic('h3')
        expected = [origin, h3, targets[0]]
        self.assertEqual(moves, expected)

    def test_get_nearest_target_knight(self):
        targets = ['g1', 'f4']
        board = self.get_custom_board(tasks.KNIGHT, 'h2', *targets)
        origin = tasks.from_algebraic('h2')
        targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_nearest_target(origin, targets)

        f3 = tasks.from_algebraic('f3')
        expected = [origin, f3, targets[0]]
        self.assertEqual(moves, expected)

    def test_get_nearest_target_rook(self):
        targets = ['b4', 'c4', 'b3', 'c3']
        board = self.get_custom_board(tasks.ROOK, 'h2', *targets)
        origin = tasks.from_algebraic('h2')
        targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_nearest_target(origin, targets)

        not_expected = tasks.from_algebraic('b4')
        self.assertNotIn(not_expected, moves)

    def test_get_nearest_target_queen(self):
        targets = ['b4', 'c4', 'b3', 'c3']
        board = self.get_custom_board(tasks.QUEEN, 'h2', *targets)
        origin = tasks.from_algebraic('h2')
        targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_nearest_target(origin, targets)

        self.assertEqual(3, len(moves))

    def test_get_fewest_moves_to_all_targets_king_2_pieces(self):
        targets = ['g4', 'h5']
        board = self.get_custom_board(tasks.KING, 'h2', *targets)
        board.targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_fewest_moves_to_all_targets()

        expected = [
            ['h3', 'g4'],
            ['h5']]
        self.assertEqual(moves, expected)

    def test_get_fewest_moves_to_all_targets_king_8(self):
        targets = ['g4', 'h5', 'a1', 'b2', 'b4', 'e6', 'h1', 'a8']
        board = self.get_custom_board(tasks.KING, 'h2', *targets)
        board.targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_fewest_moves_to_all_targets()
        expected = [
            ['h1'],
            ['h2', 'h3', 'g4'],
            ['h5'],
            ['g4', 'f5', 'e6'],
            ['d5', 'c4', 'b4'],
            ['c3', 'b2'],
            ['a1'],
            ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']]
        self.assertEqual(moves, expected)

    def test_get_fewest_moves_to_all_targets_queen(self):
        targets = ['g4', 'h5', 'a1', 'b2', 'b4', 'e6', 'h1', 'a8']
        board = self.get_custom_board(tasks.QUEEN, 'h2', *targets)
        board.targets = [tasks.from_algebraic(t) for t in targets]

        moves = board.get_fewest_moves_to_all_targets()

        expected = [
            ['h5'],
            ['g4'],
            ['b4'],
            ['b2'],
            ['a1'],
            ['h1'],
            ['a8'],
            ['c8', 'e6']]
        self.assertEqual(moves, expected)
