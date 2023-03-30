#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import math
import random
import sys
import secrets

def rotate(i, n, isize=64):
  i = (i << n)
  lower = i >> isize
  upper = i & (2**isize-1)
  i = upper | lower
  return i

key=64
keymax = 2**64-1
keymaxbit = 2**63
k = random.randint(0, keymax)
print(f'k={hex(k)}')

for i in range(0,64):
  p = random.randint(0, keymax)
  e = p
  for i in range(0, 16):
    r = k & 0xF
    k = rotate(k, (r-1) & 0xF)
    e = rotate(e, r)
    e ^= k
  print(f'p={hex(p)} e={hex(e)}, k={k}')


