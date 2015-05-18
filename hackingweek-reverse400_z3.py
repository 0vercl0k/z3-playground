#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    hackingweek-reverse400.py - Solve the hackingweek's (http://hackingweek.fr/) reverse400 task
#    (cheers to @kutioo for the idea!)
#    Copyright (C) 2015 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
import string
import sys
import hashlib

def checksum(flag, sum_):
    '''Code of the checksum used in the challenge after obfuscation removal'''
    rol_ = lambda x, y: (x << y) | (LShR(x, 32 - y))
    for i in range(len(flag)):
        sum_ = sum_ ^ ZeroExt(56, flag[i])
        sum_ = rol_(sum_, BitVecVal(7, 64))
    return sum_

def str_to_BitVecVals8(s):
    '''Generates a list of BitVecVal8 from a python string'''
    return map(
        lambda x: BitVecVal(ord(x), 8),
        list(s)
    )

def BitVecVals8_to_str(s):
    '''Generates a plain Python string from a list of BitVecVal8'''
    return ''.join(map(
        lambda x: chr(x.as_long()),
        s
    ))

def charset_bytes(x, charset = string.printable):
    '''Adds the constraints to have a byte following a specific ``charset``'''
    return Or([x == ord(c) for c in charset])

def ascii_printable(x):
    '''Adds the constraints to have an ascii printable byte'''
    return And(0x20 <= x, x <= 0x7f)

def generate_c_string(base_name, size, charset = None):
    '''Generates a sequence of byte you can use as something to simulate C strings. If ``charset`` is not None,
    the function ``charset`` will be called on every bytes. It should expect a single argument, the ``byte``, & should return
    a constraint.'''
    charset = ascii_printable if charset == None else charset
    bytes = [BitVec('%s%d' % (base_name, i), 8) for i in range(size)]
    return bytes, And(map(charset, bytes))

def get_models(s, n_max = None):
    '''Handy generator to enumerate the valid models inside a ``Solver`` instance.
    It is based on Leonardo's code here:
      https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation'''
    n = 0
    while s.check() == sat:
        if n_max != None and n >= n_max:
            break

        m = s.model()
        yield m

        # Create a new set of constraints blocking the current model
        # Note that every ``sym`` will be ``FuncDecl`` instances, that's why I'm using ``__call__`` to get back the original
        # symbolic variable
        s.add(Or([sym() != m[sym] for sym in m.decls()]))
        n += 1

    raise StopIteration

def main(argc, argv):
    '''Solution expected:
      >> 'Phoh0wauth':'3efafa3e161a756e6e1711dbceaf9d68'''
    for x in range(1, 6):
        print 'SIZE %d'.center(50, '=') % x
        prefix, suffix = map(str_to_BitVecVals8, ['P', '0wauth'])
        flag_bytes, constraints = generate_c_string('c', x, charset = charset_bytes)
        flag_bytes_complete = prefix + flag_bytes + suffix
        sum_ = checksum(flag_bytes_complete, BitVecVal(0x555555, 64))
        s = Solver()
        s.add(sum_ == 0x7fd5c3fe7ffdf7fe, constraints)
        for model in get_models(s):
            sol = BitVecVals8_to_str(prefix) + ''.join(chr(model[i].as_long()) for i in flag_bytes) + BitVecVals8_to_str(suffix)
            if hashlib.md5(sol).hexdigest() == '3efafa3e161a756e6e1711dbceaf9d68':
                print '>> %r:%r' % (sol, hashlib.md5(sol).hexdigest())
                break
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
