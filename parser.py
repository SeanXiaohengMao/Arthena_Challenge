#!/usr/bin/python
import re
import os
import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

# Define 2 dictionaries to save the data
dic = {}	# dictionary for artist: works
dicValue = {}	# dictionary for artist: totalValue

# Parse the documents
Path = "data/2017-12-20/"
filelist = os.listdir(Path)
for file in filelist:	# open the documents in the loop
    if file.endswith(".html") and file.startswith("lot"): 
        fh = open(Path+file, "r")
        num = 1
        line = fh.readline()
        while line:

        	# search the artist name in a html file
			if num == 1:
				reobj = re.search( r'<h3 class=\'artist\'>(.*?)( \(.*\))*</h3>', line)
				if reobj:
					artist = '\''+reobj.group(1)+'\''
					# initialize the dictionaries of the artist
					if not dic.has_key(artist):
						dic[artist] = [];	# the artist's works are saved as a list 
						dicValue[artist] = 0;
					num += 1

			# search the title of the work in a html file
			elif num == 2:
				reobj = re.search( r'<h3>(.*?)</h3>', line)
				if reobj:
					title = '\''+reobj.group(1)+'\''
					num += 1

			# search the price of the work in a html file
			elif num == 3:
				reobj = re.search( r'<div><span class=\'currency\'>(.*?)</span><span>(.*?)</span></div>', line)
				if reobj:
					currency = '\''+reobj.group(1)+'\''
					value = locale.atoi(reobj.group(2))	# convert string to integer
					if currency == '\'GBP\'':	# convert GBP to USD
						value *= 1.34
						currency = '\'USD\''
					dicValue[artist] += value;	# calculate the totalValue
					amount = '\''+"{:,}".format(value)+'\''
					dic[artist].append({'title': title, 'currency': currency, 'amount': amount}) #	each work is saved as a dictionary
					break

			line = fh.readline()
        fh.close()

# Print the dictionaries, structure the results into a format
print "["
for artist in dic.keys():
	print '\t{'
	print '\t\tartist: '+artist+','
	print '\t\ttotalValue: \'USD '+"{:,}".format(dicValue[artist])+'\','
	print '\t\tworks: ['
	for work in dic[artist]:
		print '\t\t\t{ title: '+work['title']+', currency: '+work['currency']+', amount: '+work['amount']+' },'
	print '\t\t],'
	print '\t},'
print "]"
 # exit;
