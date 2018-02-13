#!/usr/bin/python
import re
import os

Path = "data/2015-03-18/"
filelist = os.listdir(Path)
i = 0
dic = {}
for file in filelist:
    if file.endswith(".html") and file.startswith("lot"): 
        fh = open(Path+file, "r")
        num = 1
        line = fh.readline()
        while line:
			if num == 1:
				reobj = re.search( r'<h2>(.*?)( \(.*\))*</h2>', line)
				if reobj:
					artist = '\''+reobj.group(1)+'\''
					if not dic.has_key(artist):
						dic[artist] = [];
					num += 1
			elif num == 2:
				reobj = re.search( r'<h3>(.*?)</h3>', line)
				if reobj:
					dic[artist].append('\''+reobj.group(1)+'\'')
					num += 1
					break
			line = fh.readline()
        fh.close()



print "["
for artist in dic.keys():
	print '\t{'
	print '\t\tartist: '+artist+','
	print '\t\tworks: ['+', '.join(dic[artist])+'],'
	print '\t},'
print "]"
 # exit;
