#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import math
import random
import sys
import secrets

def lsb(i, n):
  mask = 2**n - 1
  i2 = i & mask
  return i2

def msb(i, n, isize=64):
  i2 = i & (2**isize - 1)
  i3 = i2 >> (isize-n)
  return i3

def getbits(i, ubit=0, lbit=0):
  numbits = ubit-lbit+1
  bits = msb(i, numbits, ubit+1)
  return bits

def getbit(i, bitpos=0):
  return getbits(i, bitpos, bitpos)

def invert(i, n=64):
  mask = 2**n - 1
  i2 = i ^ mask
  return i2


def rotl(i, n, isize=64):
  i2 = (i << n)
  lower = i2 >> isize
  upper = i2 & (2**isize-1)
  i3 = upper | lower
  return i3

def rev(i, n, isize=64):
  for b in range(n):
    lower = b
    upper = n-b-1
    if lower >= upper:
      break
    lbit = getbit(i, lower)
    ubit = getbit(i, upper)
    mask = invert(1<<upper | 1 << lower, isize)
    ii = i
    i &= mask
    tmp = lbit<<upper | ubit<<lower
    i |= tmp
  return i


def jumble(v, k, n=16, isize=64, id='x'):
  v1 = v
  for i in range(n):
    rotupperbit = (i+1)*4
    rot = msb(k, 4, rotupperbit) + 1
    invbit = msb(k, 1, (i+1)*3%64)
    revbit = msb(k, 1, (i+1)*7%64)
    v2 = rotl(v1, rot, isize)
    v3 = v2 ^ k
    v4 = invert(v3, isize) if invbit==0 else v3
    v5 = rev(v4, isize) if revbit==0 else v4
    v1 = v5
  v6 = rev(v1, isize)
  return v6


def enc(v, k, n=2, isize=64):
  k = jumble(k, k, n, isize, 'k')
  e = jumble(plain, k, n, isize, 'p')
  return e, k


isize = 64
imax = 2**64-1
k = random.randint(0,imax)
msglen = 5000
#msg = [random.randint(0,imax) for i in range(msglen)]
msg = [i for i in range(msglen)]
msg = [0 for i in range(msglen)]
for plain in msg:
  e, k = enc(plain, k)
  print(f'p={plain:016x} e={e:016x}, k={k:016x}')


