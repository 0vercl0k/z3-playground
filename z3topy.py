#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    z3topy.py - This script aims at converting a Z3 expression to a plain
#    Python function.
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

def z3_to_py_bv_32(expr):
    assert(is_bv(expr))
    trans = {
        '+' : '+',
        '-' : '-',
        '^' : '^',
        '*' : '*',
        '/' : '/',
        'LShR' : '>>',
        '<<': '<<',
        '&' : '&',
        '|' : '|',
        '~' : '~',
        'Extract' : 'Extract',
        'Concat' : 'Concat'
    }

    decl = '%r' % expr.decl()
    args = [expr.arg(i) for i in range(expr.num_args())]
    results = [z3_to_py_bv_32(i) for i in args]
    if expr.num_args() == 0:
        if isinstance(expr, BitVecNumRef):
            return expr.as_string()
        return decl
    elif expr.num_args() == 1:
        if decl == 'Extract':
            h = Z3_get_decl_int_parameter(expr.ctx_ref(), expr.decl().ast, 0)
            l = Z3_get_decl_int_parameter(expr.ctx_ref(), expr.decl().ast, 1)
            return '((' +  results[0] + ' >> %d) & ((2**(%d + 1) - 1)))' % (l, h)
        else:
            return trans[decl] + results[0]
    else:
        if trans[decl] == 'Concat':
            return '((%s << %d) | %s)' % (
                results[0], args[1].size(), results[1]
            )
        else:
            return '(%s %s %s)' % (results[0], trans[decl], results[1])

def main(argc, argv):
    a, b = BitVecs('a b', 32)
    x = LShR(a * b, b) + 1337 << 2 * (a + b << 1) & 0xf
    print z3_to_py_bv_32(x * 2)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))