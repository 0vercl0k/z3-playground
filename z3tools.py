#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    z3tools.py - This script aims at keeping "important" / high-level functionalities
#    you usually need when using Z3. Hopefully, at some point I'll have enough of those
#    to call it a ``library``, maybe not!
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
import unittest
import string
from z3 import *

# >> VS LShR
BitVecRef.__rshift__ = LShR

def prove_(f):
    '''Taken from http://rise4fun.com/Z3Py/tutorialcontent/guide#h26'''
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        return True
    return False

def to_SMT2(f, statu s = 'unknown', name = '', logic = ''):
    '''https://stackoverflow.com/questions/14628279/z3-convert-z3py-expression-to-smt-lib2'''
    v = (Ast * 0)()
    return Z3_benchmark_to_smtlib_string(f.ctx_ref(), name, logic, status, '', 0, v, f.as_ast())

def abs_z3(a):
    '''Get the absolute value of a Z3 variable'''
    return If(a >= 0, a, -a)

def BitVec_to_bool(bv):
    '''Transforms the BitVec ``bv`` into a Boolean'''
    return If(bv == 1, BoolVal(True), BoolVal(False))

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

class TestZ3tools(unittest.TestCase):
    def test_BitVec_to_bool(self):
        self.assertEqual(is_bool(simplify(BitVec_to_bool(BitVecVal(10, 32)))), True)
        self.assertEqual(simplify(BitVec_to_bool(BitVecVal(10, 64))), True)
        self.assertEqual(simplify(BitVec_to_bool(BitVecVal(0, 8))), False)

    def test_str_to_BitVecVals8(self):
        self.assertEqual(''.join(chr(x.as_long()) for x in str_to_BitVecVals8('hello-w0rldz!1')), 'hello-w0rldz!1')

    def test_BitVecVals8_to_str(self):
        self.assertEqual(BitVecVals8_to_str(str_to_BitVecVals8('hello-w0rldz!1')), 'hello-w0rldz!1')

    def test_generate_c_string(self):
        c, eq = generate_c_string('test1', 10)
        self.assertEqual(len(c), 10)
        s = Solver()
        s.push()
        s.add(eq, Distinct(c))
        models = get_models(s, 100)
        for model in models:
            syms = map(lambda s: chr(model[s].as_long()), c)
            self.assertEqual(filter(lambda x: x in string.printable, syms), syms)
        s.pop()
        s.push()
        c, eq = generate_c_string(
            'test2',
            10,
            lambda c: And(c >= 0x41, c <= 0x5a)
        )
        s.add(eq, Distinct(c))
        models = get_models(s, 100)
        for model in models:
            syms = map(lambda sym: chr(model[sym].as_long()), c)
            self.assertEqual(filter(lambda x: x in string.uppercase, syms), syms)
        s.pop()
        s.push()
        c, eq = generate_c_string(
            'test3',
            10,
            lambda x : charset_bytes(**{'x' : x, 'charset' : ['A', 'B']})
        )
        for model in models:
            syms = map(lambda sym: chr(model[sym].as_long()), c)
            self.assertEqual(filter(lambda x: x in ['A', 'B'], syms), syms)

    def test_get_modesl(self):
        s = Solver()
        a = Int('a')
        s.add(a > 0)
        s.push()
        s.add(a < 10)
        models = map(lambda m: m[a].as_long(), get_models(s))
        self.assertEqual(set(models), set(range(1, 10)))
        s.pop()
        s.add(a < 5)
        models = map(lambda m: m[a].as_long(), get_models(s))
        self.assertEqual(set(models), set(range(1, 5)))

def main(argc, argv):
    unittest.main()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
