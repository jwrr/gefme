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


def getnibble(i, n):
  nibble = getbits(i, n*4+3, n*4)
  return nibble


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


def rotr(i, n, isize=64):
  upper = getbits(i, n-1, 0) << (isize-n)
  mask = 2**(isize-n) - 1
  lower = (i >> n) & mask
  final = upper | lower
  return final


def swapbits(i, a, b, isize=64):
  abit = getbit(i, a)
  bbit = getbit(i, b)
  mask = invert(1<<a | 1 << b, isize)
  i &= mask
  tmp = bbit<<a | abit<<b
  i |= tmp
  return i


def rev(i, n, isize=64):
  for b in range(n):
    lower = b
    upper = n-b-1
    if lower >= upper:
      break
    i = swapbits(i, lower, upper, isize)
  return i


def prime(i):
      #0  1  2  3   4   5   6   7   8   9  10  11  12  13  14  15  16    17  18  19  20  21  22  23  24   25
  p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,   61, 67, 71, 73, 79, 83, 89, 97, 101, 
       103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 
       223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 
       347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 
       463, 467, 479, 487, 491, 499, 503, 509, 521]
  return p[i]


def getcmd(k, i):
  cmd = getnibble(k, i) + 1
  rot_cmd = prime(cmd)
  inv_cmd = getbit(k, cmd*3%isize)
  rev_cmd = getbit(k, cmd*7%isize)
  return rot_cmd, inv_cmd, rev_cmd


def jumble(v, k, n=2, isize=64, id='x'):
  for i in range(n):
    rot_cmd, inv_cmd, rev_cmd = getcmd(k, i)
    v = rotl(v, rot_cmd, isize)
    v = invert(v, isize) if inv_cmd==0 else v
    v = rev(v, isize) if rev_cmd==0 else v
    v = v ^ k
  return v


def unjumble(v, k, n=2, isize=64, id='x'):
  for i in range(n-1, -1, -1):
    rot_cmd, inv_cmd, rev_cmd = getcmd(k, i)
    v = v ^ k
    v = rev(v, isize) if rev_cmd==0 else v
    v = invert(v, isize) if inv_cmd==0 else v
    v = rotr(v, rot_cmd, isize)
  return v


def enc(v, k, n=2, isize=64):
  k1 = jumble(k, k, n, isize, 'k')
  if k1 == k:
    k1 = rotl(k1, 61, isize)
    k1 = rev(k1, isize)
    k1 = invert(k1, isize)
  k = k1
  e = jumble(plain, k, n, isize, 'p')
  return e, k


def dec(e, k, n=2, isize=64):
  k1 = jumble(k, k, n, isize, 'k')
  if k1 == k:
    print("BADKEY ")
    k1 = rotl(k1, 61, isize)
    k1 = rev(k1, isize)
    k1 = invert(k1, isize)
  k = k1
  p = unjumble(e, k, n, isize, 'p')
  return p, k

## --------------------------------------------------
## --------------------------------------------------

isize = 64
imax = 2**64-1
k1 = 0x380ec3dc4fe9e477 # random.randint(0,imax)
msglen = 500
#msg = [random.randint(0,imax) for i in range(msglen)]
pmsg = [i for i in range(msglen)]
pmsg = [0 for i in range(msglen)]
n = 2

emsg = []
kmsg = []
k = k1
for plain in pmsg:
  e, k = enc(plain, k, n, isize)
  emsg.append(e)
  kmsg.append(k)

dmsg = []
k = k1
for e in emsg:
  p, k = dec(e, k, n, isize)
  dmsg.append(p)

print(f'k1=0x{k1:016x}')
for i, p in enumerate(pmsg):
  d = dmsg[i]
  e = emsg[i]
  k = kmsg[i]
  print(f'p={p:016x} k={k:016x} e={e:016x} d={d:016x}')

