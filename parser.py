#!/usr/bin/python
import re
import os
import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

Path = "data/2017-12-20/"
filelist = os.listdir(Path)
dic = {}
dicValue = {}
for file in filelist:
    if file.endswith(".html") and file.startswith("lot"): 
        fh = open(Path+file, "r")
        num = 1
        line = fh.readline()
        while line:
			if num == 1:
				reobj = re.search( r'<h3 class=\'artist\'>(.*?)( \(.*\))*</h3>', line)
				if reobj:
					artist = '\''+reobj.group(1)+'\''
					if not dic.has_key(artist):
						dic[artist] = [];
						dicValue[artist] = 0;
					num += 1
			elif num == 2:
				reobj = re.search( r'<h3>(.*?)</h3>', line)
				if reobj:
					title = '\''+reobj.group(1)+'\''
					num += 1
			elif num == 3:
				reobj = re.search( r'<div><span class=\'currency\'>(.*?)</span><span>(.*?)</span></div>', line)
				if reobj:
					currency = '\''+reobj.group(1)+'\''
					value = locale.atoi(reobj.group(2))
					if currency == '\'GBP\'':
						value *= 1.34
						currency = '\'USD\''
					dicValue[artist] += value;
					amount = '\''+"{:,}".format(value)+'\''
					dic[artist].append({'title': title, 'currency': currency, 'amount': amount})
					break
			line = fh.readline()
        fh.close()

print "["
for artist in dic.keys():
	print '\t{'
	print '\t\tartist: '+artist+','
	print '\t\ttotalValue: \'USD '+"{:,}".format(dicValue[artist])+'\','
	print '\t\tworks:',
	for work in dic[artist]:
		print '['
		print '\t\t\t{ title: '+work['title']+', currency: '+work['currency']+', amount: '+work['amount']+' },' 
		print '\t\t],'
	print '\t},'
print "]"
 # exit;
