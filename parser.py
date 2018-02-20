#!/usr/bin/python
import re
import os
import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

'''
 Define 2 dictionaries to save the data,
 dic is dictionary of artist: works, 
 dicValue is dictionary of artist: totalValue.
'''
dic = {}	
dicValue = {}	

''' 
 Parse the documents,
 open the documents in the loop
'''
Path = "data/2017-12-20/"
filelist = os.listdir(Path)
for file in filelist:	
    if file.endswith(".html") and file.startswith("lot"): 
		fh = open(Path+file, "r")
		num = 1
		line = fh.readline()
        # search line by line
		while line:

			# ''' search the artist name in a html file '''
			if num == 1:
				reobj = re.search( r'<h3 class=\'artist\'>(.*?)( \(.*\))*</h3>', line)
				if reobj:
					artist = '\''+reobj.group(1)+'\''
					# initialize the dictionaries of the artist
					if artist not in dic:
						# the artist's works are saved as a list 
						dic[artist] = []	
						dicValue[artist] = 0
					num += 1

			# ''' search the title of the work in a html file '''
			elif num == 2:
				reobj = re.search( r'<h3>(.*?)</h3>', line)
				if reobj:
					title = '\''+reobj.group(1)+'\''
					num += 1

			# '''
			#  search the price of the work in a html file
			#  each work is saved as a dictionary
			# '''
			elif num == 3:
				reobj = re.search( r'<div><span class=\'currency\'>(.*?)</span><span>(.*?)</span></div>', line)
				if reobj:
					currency = '\''+reobj.group(1)+'\''
					# convert string to integer
					value = locale.atoi(reobj.group(2))	
					# convert GBP to USD
					if currency == '\'GBP\'':	
						value *= 1.34
						currency = '\'USD\''
					# calculate the totalValue
					dicValue[artist] += value;	
					amount = '\''+"{:,}".format(value)+'\''
					dic[artist].append({'title': title, 'currency': currency, 'amount': amount}) 
					break

			line = fh.readline()
		fh.close()

'''
 Print the dictionaries.
 Structure the results into the format.
'''
print "["
for ia, artist in enumerate(dic.keys()):
	print '    {'
	print '        artist: '+artist+','
	print '        totalValue: \'USD '+"{:,}".format(dicValue[artist])+'\','
	print '        works: ['
	for i, work in enumerate(dic[artist]):
		print '            { title: '+work['title']+', currency: '+work['currency']+', amount: '+work['amount']+' }',
		if i != len(dic[artist]) - 1:
			print ','
		else:
			print
	print '        ]'
	if ia != len(dic.keys()) - 1:
		print '    },'
	else:
		print '    }'
print "]"
 # exit;
