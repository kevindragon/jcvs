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
    filelist = map(lambda x: string.strip(x.replace("\\", "\/"), "\\\/\r\n "),
                   open(filename, 'r').readlines())
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

notexistfile = []
# 检查文件列表是否正确
for index, line in enumerate(filelist):
    if "" == line:
        continue
    if has_revision(line):
        filelist[index] = line[:line.rfind(' ')]
    if not os.path.exists(filelist[index]):
        notexistfile.append(filelist[index])
        del filelist[index]
    if '' == line or 0 == line.find('#'):
        del filelist[index]

for f in filelist:
    if "" == f:
        continue
    # 取本地文件CVS/Entries文件里的版本号
    rev_names = get_local_rev(f, cvspath)
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