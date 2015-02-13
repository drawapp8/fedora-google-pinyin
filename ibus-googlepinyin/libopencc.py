#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
'''wrapper of libopencc

opencc is a library for converting character between traditional chinese and simplified chinese.

@author: Jiahua Huang <jhuangjiahua@gmail.com>
@license: LGPLv3+
@see: opencc
'''

import ctypes
import ctypes.util
import sys

libc = ctypes.CDLL(ctypes.util.find_library('c'))
opencc = ctypes.CDLL(ctypes.util.find_library('opencc'))
od = opencc.opencc_open('zhs2zht.ini')

def convert(text):
    '''convert simplified chinese to traditional chinese
    '''
    ret = ctypes.c_char_p(opencc.opencc_convert_utf8(od, text, -1))
    stri = ret.value
    libc.free(ret)
    return stri


if __name__=="__main__":
    if sys.argv[1:]:
        text = ' '.join(sys.argv[1:])
        pass
    else:
        text = sys.stdin.read()
        pass
    print convert(text)
