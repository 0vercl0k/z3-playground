#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    if-then-else.py - 
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

from z3 import *

a_, b_ = BitVecs('a_ b_', 32)
a = If(ULT(a_ + b_, 100), a_ + BitVecVal(100, 32), BitVecVal(1337, 32))
b = If(ULT(a_ + b_, 100), b_ - BitVecVal(10, 32), b_ + BitVecVal(1000, 32))
solve(UGT(a, 1337), b == 0xdeadbeef)