#!/usr/bin/env python
# encoding=utf-8

import sys
import os
import config
from fun import *

if 2 > len(sys.argv):
    print 'please specify a file'
    sys.exit(1)
else :
    input_file = sys.argv[1]

try :
    files = [ x.strip('/\r\n ') for x in open(input_file, 'r') if (x.strip() != '' and x.find('#') != 0) ]
except ValueError:
    print input_file + ' not found'
    sys.exit(1)

CVSROOTDIR = config.cvspath
CURRENTDIR = os.getcwd()
os.chdir(CVSROOTDIR)

for fr in files:
    if '' == fr:
        continue

    tmpfileline = fr.split(' ')
    f = tmpfileline[0]
    r = tmpfileline[1]
    # 获取文件列表里面文件的主版本号
    oriRevs = r.split('.');
    oriBaseRev = ".".join(oriRevs[0:-2])
        
    cmd = 'cvs log %s' % f
    cmdres = execk(cmd)
    revs = []
    flag = False
    for line in cmdres:
        line = line.strip('\r\n ')
        if flag and 0 == line.find('revision'):
            tmprev = line[len('revision '):]
            revs.append(tmprev)
        if line == '----------------------------':
            flag = True
        else:
            flag = False

    # 循环所有版本号，查找给出的文件列表里面的更新
    for v in revs:
        new_rev = 0
        if 0 == v.find(oriBaseRev) and (0 == len(v.split('.')) - len(r.split('.'))):
            tmpr = r.split(".")
            rSuffix = tmpr[-2] + "." + tmpr[-1]
            tmpv = v.split(".")
            vSuffix = tmpv[-2] + "." + tmpv[-1]
            if vSuffix > rSuffix:
                is_new = 'Y'
                new_rev = v
                break
            else:
                is_new = 'N'

    print is_new, "/"+fr, 
    if 0 < new_rev:
        print new_rev
    else:
        print

os.chdir(CURRENTDIR)
