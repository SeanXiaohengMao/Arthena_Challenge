#!/usr/bin/python
import re
import os
import sys

Path = "data/2015-03-18/"
filelist = os.listdir(Path)
sys.stdout.write("[")
i = 0
for file in filelist:
    if file.endswith(".html") and file.startswith("lot"): 
        fh = open(Path+file, "r")
        line = fh.readline()
        while line:
			reobj = re.search( r'<h2>(.*?)( \(.*\))*</h2>', line)
			if reobj:
				if i:
					sys.stdout.write(", ")
				sys.stdout.write('\''+reobj.group(1)+'\'')
				i = 1
				break
			line = fh.readline()
        fh.close()
sys.stdout.write("]\n")
 # exit;
