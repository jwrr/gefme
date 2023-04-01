#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import math
import os
import random
import re
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
       463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
  return p[i]


def getcmd(k, i, isize=64):
  ptr = getnibble(k, i)
  cmd = getnibble(k, ptr) + 1
  rot_cmd = prime(cmd)
  add_cmd = (cmd & 0x7) + 1
  inv_cmd = getbit(k, cmd*3%isize)
  rev_cmd = getbit(k, cmd*7%isize)
  return rot_cmd, inv_cmd, rev_cmd, add_cmd


def add(val, n, wid = 4, isize=64):
  m = 2**wid - 1
  for i in range(0, isize, wid):
    v = getbits(val, i+wid-1, i) + n
    v = (v & m) << i
    mshifted = invert(m << i, isize)
    val = (val & mshifted) | v
  return val


def jumble(v, k, n=2, isize=64, id='x'):
  for i in range(n):
    rot_cmd, inv_cmd, rev_cmd, add_cmd = getcmd(k, i, isize)
    v = add(v, add_cmd, 4, isize)
    v = rotl(v, rot_cmd, isize)
    v = invert(v, isize) if inv_cmd==0 else v
#     v = rev(v, isize)
    v = v ^ k
  return v


def unjumble(v, k, n=2, isize=64, id='x'):
  for i in range(n-1, -1, -1):
    rot_cmd, inv_cmd, rev_cmd, add_cmd = getcmd(k, i, isize)
    v = v ^ k
#     v = rev(v, isize)
    v = invert(v, isize) if inv_cmd==0 else v
    v = rotr(v, rot_cmd, isize)
    v = add(v, -add_cmd, 4, isize)
  return v


def encword(plain, k, n=2, isize=64):
  k1 = jumble(k, 0, n, isize, 'k')
  k = k1
  e = jumble(plain, k, n, isize, 'p')
  return e, k

def encmsg(pmsg, k , n=1, isize=64):
  emsg = []
  kmsg = []
  for plain in pmsg:
    e, k = encword(plain, k, n, isize)
    emsg.append(e)
    kmsg.append(k)
  return emsg, kmsg


def decword(e, k, n=2, isize=64):
  k1 = jumble(k, 0, n, isize, 'k')
  k = k1
  plain = unjumble(e, k, n, isize, 'p')
  return plain, k


def decmsg(emsg, k, n=1, isize=64):
  dmsg = []
  for e in emsg:
    p, k = decword(e, k, n, isize)
    dmsg.append(p)
  return dmsg


def test():
  isize = 64
  imax = 2**64-1
  k1 = 0x380ec3dc4fe9e477 # random.randint(0,imax)
  msglen = 100
  #msg = [random.randint(0,imax) for i in range(msglen)]
  pmsg = [i for i in range(msglen)]
  pmsg = [0 for i in range(msglen)]
  n = 1

  emsg, kmsg = encmsg(pmsg, k1, n, isize)
  dmsg = decmsg(emsg, k1, n, isize)

  print(f'k1=0x{k1:016x}')
  for i, p in enumerate(pmsg):
    d = dmsg[i]
    e = emsg[i]
    k = kmsg[i]
    print(f'p={p:016x} k={k:016x} e={e:016x} d={d:016x}')
  return


def read64bit(filename):
  data = []
  filesize = os.path.getsize(filename)
  try:
    with open(filename, 'rb') as f:
      b8 = f.read(8)
      while b8:
        i = int.from_bytes(b8, byteorder='little')
        data.append(i)
        b8 = f.read(8)
  except FileNotFoundError:
    return []
  return data, filesize


def write64bit(filename, data, filesize):
  with open(filename, 'wb') as f:
    for i in data:
      numbytes = min(8, filesize) if filesize >= 0 else 8
      m = 2**(numbytes*8) - 1
      i = i & m
      f.write((i).to_bytes(numbytes, byteorder='little', signed=False))
      filesize -= 8
  return


def main(filelist):
  k = 0x380ec3dc4fe9e477 # random.randint(0,imax)
  for filename in filelist:
    data, filesize = read64bit(filename)
    if len(data) == 0:
      print(f'error: {filename}')
    elif filename.endswith('.gef'):
      ofilename = re.sub('.gef$', '', filename)
      dmsg = decmsg(data, k)
      filesize = dmsg.pop(0)
      print(f'decode: {filename} -> {ofilename}. filesize = {filesize}')
      write64bit(ofilename, dmsg, filesize)
      os.remove(filename)
    else:
      ofilename = filename+'.gef'
      print(f'encode: {filename} -> {ofilename}. filesize = {filesize}')
      data.insert(0, filesize)
      emsg, kmsg = encmsg(data, k)
      write64bit(ofilename, emsg, len(emsg)*8)
      os.remove(filename)
  return



## --------------------------------------------------
## --------------------------------------------------

# test()

main(sys.argv[1:])
