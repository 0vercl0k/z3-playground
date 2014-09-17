#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    hash_collisions_z3.py - Using z3py to satisfy a bunch of constraints involving
#    a non-cryptographic hashing algorithm.
#    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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

def H(input_bytes):
    '''This idea comes directly from awesome James Forshaw, read his blogpost:
    http://tyranidslair.blogspot.co.uk/2014/09/generating-hash-collisions.html'''
    h = 0
    for byte in input_bytes:
        h = h * 31 + ZeroExt(24, byte)
    return h

def ascii_printable(x):
    '''Adds the constraints to have an ascii printable byte'''
    return And(0x20 <= (x & 0xff), (x & 0xff) <= 0x7f)

def generate_ascii_printable_string(base_name, size, solver):
    '''Generates a sequence of byte you can use as something to simulate C strings,
    and also adds to the solver the required constraints to have an ascii printable string'''
    bytes = [BitVec('%s%d' % (base_name, i), 8) for i in range(size)]
    for byte in bytes:
        solver.add(ascii_printable(byte))
    return bytes

def str_to_BitVecVals8(s):
    '''Generates a list of BitVecVal8 from a python string'''
    return map(
        lambda x: BitVecVal(ord(x), 8),
        list(s)
    )

def collide(target_str, base_str):
    '''Generates a string with the following properties:
        * strcmp(res, base_str) = 0
        * H(res) == H(target_str)'''
    size_suffix = 7
    s = Solver()
    # We can even impress girls by having an ascii printable suffix :-)))
    res = str_to_BitVecVals8(base_str) + [BitVecVal(0, 8)] + generate_ascii_printable_string('res', size_suffix, s)
    s.add(H(res) == H(str_to_BitVecVals8(target_str)))
    if s.check() == sat:
        x = s.model()
        return base_str + '\x00' + ''.join(chr(x[i].as_long()) for i in res[-size_suffix:])
    raise Exception('Unsat!')

def main(argc, argv):
    '''Ready to roll!'''
    a = 'xyz'
    b = 'abc'
    c = collide(a, b)
    print 'c = %r' % c
    print 'H(%r) == H(%r)' % (a, c)
    print 'strcmp(%r, %r) = 0' % (c, b)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))