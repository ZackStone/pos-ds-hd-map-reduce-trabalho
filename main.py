import mincemeat
import glob
import csv

text_files = glob.glob('files/*')

def file_contents(file_name):
	f = open(file_name)
	try:
		return f.read()
	finally:
		f.close()

source = dict((file_name, file_contents(file_name)) for file_name in text_files)

def mapfn(k, v):
	print 'map ' + k
	from stopwords import allStopWords
	for line in v.splitlines():
		for word in line.split():
			if (word not in allStopWords):
				yield word, 1

def reducefn(k, v):
	#print 'reduce ' + k
	return sum(v)

print 'instancia server'
s = mincemeat.Server()

print 'define atributos do server'
# A fonte de dados pode ser qualquer objeto do tipo dicionario
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

print 'run server'
results = s.run_server(password="changeme")

print 'write results'
#w = csv.writer(open("result.csv", 'w'))
for k, v in results.items():
	#w.writerow([k, v])
	print('#######################################')
	print('k')
	print(k)
	print('v')
	print(v)

print 'fim'