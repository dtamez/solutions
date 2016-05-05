#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Danny Tamez <zematynnad@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Algorithm for returning a list of moves (defined in algebraic notation) given
a starting square and a piece type.
"""
from __future__ import absolute_import

import argparse


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
