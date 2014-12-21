#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    backtracking.py - 
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

a, b = BitVecs('a b', 32)
s = Solver()
s.add(a + b == 1337)
s.push()
s.add(a*a == 32)
print s
print s.check()

s.pop()
print s
print s.check()
print s.model()
print (469762080 + 3825206553) & 0xffffffff