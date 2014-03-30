#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    proof_unsigned_integer_overflow_check.py - I figured I should actually prove that the "trick"
#    I was using to detect integer overflow when adding two unsigned integers is actually right :)
#    (and it was the perfect occasion to mess with z3py :P)
#    Copyright (C) 2014 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
from z3 import *

def does_overflow_custom_check(a, b):
    '''I used that check for quite a while without never
    actually proving it is working for the integers:
    an occasion to write some z3-magic!'''
    return If(
        ULT((a + b), a), # ULT = < unsigned
        True,
        False
    )

def does_overflow_check(a, b):
    '''The boring way, where you have to use a greater type to store
    the temporary result'''
    a_64 = ZeroExt(32, a)
    b_64 = ZeroExt(32, b)
    return If(
        UGE((a_64 + b_64), BitVecVal(0x100000000, 64)), # UGE = >= unsigned
        True,
        False
    )

def main(argc, argv):
    x, y = BitVecs('a b', 32)
    prove(
        does_overflow_check(x, y) ==
        does_overflow_custom_check(x, y)
    )
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))