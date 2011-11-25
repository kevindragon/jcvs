#!/usr/bin/env python
# encoding=utf-8

import sys
import os
import string
import re

def execk(cmd):
    "执行一个命令"
    pp = os.popen(cmd, 'r')
    res = pp.readlines()
    return res #''.join(res)

if 2 > len(sys.argv):
    print 'please specify a file'
    sys.exit(1)
else :
    input_file = sys.argv[1]

try :
    files = [ x.strip('\r\n ') for x in open(input_file, 'r') if (x.strip() != '' and x.find('#') != 0) ]
except ValueError:
    print input_file + ' not found'
    sys.exit(1)

CVSROOTDIR = '/home/www/kevin/alpha/'
CURRENTDIR = os.getcwd()

os.chdir(CVSROOTDIR)

for fr in files:
    if '' == fr:
        continue

    tmpfileline = fr.split(' ')
    f = tmpfileline[0]
    tmpr = tmpfileline[1].split('.')
    r = float(tmpr[0] + '.' + tmpr[1])
        
    cmd = 'cvs log %s' % f
    cmdres = execk(cmd)
    revs = []
    flag = False
    for line in cmdres:
        line = line.strip('\r\n ')
        if flag and 0 == line.find('revision'):
            tmprev = line[len('revision '):].split('.')
            revs.append(round(float(tmprev[0] + '.' + tmprev[1]), 2))
        if line == '----------------------------':
            flag = True
        else:
            flag = False

    if revs[0] - r > 0.1:
        is_new = 'Y'
    else:
        is_new = 'N'

    print is_new, revs[0], r, fr

os.chdir(CURRENTDIR)
