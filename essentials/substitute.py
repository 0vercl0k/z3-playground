#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    substitute.py - 
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

a, b = BitVec('a', 32), BitVecVal(1, 32)
c = a + a + b
print c

print substitute(c, (a, BitVecVal(1337, 32)), (b, BitVec('z', 32)))
print 1337*2