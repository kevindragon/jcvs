#!/usr/bin/env python

import os
import sys
import config
from fun import *

if 3 > len(sys.argv):
    print 'please specify a tag name'
    sys.exit(1)

filename = sys.argv[1]
if not os.path.exists(filename):
    print 'the file: %s does not exists' % filename
    sys.exit(1)

tag_name = sys.argv[2]

# comments
if len(sys.argv) > 3:
    comments = sys.argv[3]
else:
    comments = ''

filelist = [ x.strip("\r\n ") for x in open(filename, 'r') if (0 != x.find('#') and '' != x.strip()) ]

shell_template = """#!/bin/bash

CVSROOTDIR="%s"
CURRENTDIR=`pwd`

cd $CVSROOTDIR

%s

cd $CURRENTDIR

sed -i 's/^\(cvs.*\)/# \\1/g' $0
"""

notexistfile = []

subcmd = []
for file in filelist:
    
    if has_revision(file):
        file = file[:file.rfind(' ')]
        
    if not os.path.exists(config.cvspath + file):
        notexistfile.append(file)
        continue

    subcmd.append(('cvs tag -b "%s" "%s" | tee -a tag.log\n'  
                  'cvs up -r "%s" "%s" | tee -a tag.log\n'  
                  'cvs ci -m "%s" "%s" | tee -a tag.log') % \
                 (tag_name, file, tag_name, file, comments, file))

shell = shell_template % (config.cvspath, "\n".join(subcmd))

print shell

print "\n".join(notexistfile)
