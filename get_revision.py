#!/usr/bin/env python
# encoding=utf-8
# filename: get_revision.py

import os, sys, string
import config
from fun import *

USAGE = """
get_revision.py filename [1,2,3]
"""

if config.cvspath == '' or not os.path.exists(config.cvspath):
    print 'Please sepcify you workpath where is your local cvs repostory'
    exit()

if 2 > len(sys.argv):
    print 'Please specify a file contain a file list'
    print USAGE
    exit()

filename = sys.argv[1]
# 获取输入文件里的文件列表
try:
    filelist = [x.strip("\\\/\r\n").replace("\\", "\/") for x in open(filename, 'r')]
except ValueError:
    print filename, " was not found"
    exit()

# 输出参数
if len(sys.argv) > 2:
    is_show_extra = sys.argv[2]
else:
    is_show_extra = 2

# 设置本地的cvs目录
cvspath = config.cvspath
# 保存当前路径
workpath = os.getcwd()

# 切换到cvs目录
os.chdir(cvspath)

cvs_errs = []
notexistfile = []
# 检查文件列表是否正确
for index, line in enumerate(filelist):
    f = line
    if '' == f or 0 == f.find('#'):
        continue
    
    if has_revision(f):
        f = line[:f.rfind(' ')]
        
    if not os.path.exists(f):
        notexistfile.append(f)
        continue

    # 取本地文件CVS/Entries文件里的版本号
    rev_names = get_local_rev(f, cvspath)
    if None == rev_names[0]:
        cvs_errs.append(f)
        continue

    # 如果分支名称空，则是主分支HEAD
    if '' == rev_names[1]:
        rev_names[1] = 'HEAD'
    # 粗略检查文件是否发动
    if rev_names[2] != rev_names[3]:
        is_modify = 'M'
    else:
        is_modify = 'U'
    
    # 判断参数，选择输出格式
    if '0' == is_show_extra:
        print "/%s" % f
    elif '1' == is_show_extra:
        print "/%s" % f, rev_names[0]
    elif '2' == is_show_extra:
        print "/%s" % f, rev_names[0], rev_names[1]
    else:
        print is_modify, "/%s" % f, rev_names[0], rev_names[1]

# 恢复工作目录
os.chdir(workpath)

if len(notexistfile):
    print "\nnot exists files:\n" + "\n".join(notexistfile)
if len(cvs_errs):
    print "\ncvs read error:\n" + "\n".join(cvs_errs)
