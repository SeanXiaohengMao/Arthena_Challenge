#!/usr/bin/python
import re
import os

# class Artwork:
# 	def __init__(self, title, price):
# 		self.title = title
# 		self.price = price

Path = "data/2015-03-18/"
filelist = os.listdir(Path)
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
					title = '\''+reobj.group(1)+'\''
					num += 1
			elif num == 3:
				reobj = re.search( r'<div>(.*?)</div>', line)
				if reobj:
					price = '\''+reobj.group(1)+'\''
					dic[artist].append({'title': title, 'price': price})
					break
			line = fh.readline()
        fh.close()

print "["
for artist in dic.keys():
	print '\t{'
	print '\t\tartist: '+artist+','
	print '\t\tworks: ['
	for work in dic[artist]:
		print '\t\t\t{ title: '+work['title']+', price: '+work['price']+' },' 
	print '\t\t],'
	print '\t},'
print "]"
 # exit;
