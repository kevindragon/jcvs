#!/usr/bin/env python
# encoding=utf-8
# filename: fun.py

import os, string, re, time

def has_revision(line):
    line = string.strip(line)
    last_char = line[-1]
    if '9' > last_char >= '0':
        return True
    else:
        return False

def get_local_rev(filename, cvspath):
    rev_name = ['', '', '', '']
    # 从本地cvs目录读取文件版本号和分支号，本地文件名为CVS/Entries
    filepath = os.path.split(filename)
    rev_source_file = cvspath + filepath[0] + "/CVS/Entries"
    # 读取存放版本信息的文件
    try:
        revs_lines = map(lambda x: string.strip(x),
                         open(rev_source_file, 'r').readlines())
        for line in revs_lines:
            if 0 == line.find("/%s/" % filepath[1]):
                p = re.compile("/(.*)/(.*)/(.*)/(.*)/(.*)")
                match = p.match(line)
                try:
                    founds = [match.groups(0)[1], 
                              match.groups(0)[4][1:], 
                              match.groups(0)[2], 
                              time.ctime(os.stat(filename).st_mtime - 28800)]
                    rev_name = founds
                except Exception, e:
                    print e
                break
    except Exception, e:
        print rev_source_file, " not found"
        rev_name = [None] * 4
    return rev_name
