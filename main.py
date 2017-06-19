import mincemeat
import glob
import csv
import operator

text_files = glob.glob('files/*')

def file_contents(file_name):
	f = open(file_name)
	try:
		return f.read()
	finally:
		f.close()

source = dict((file_name, file_contents(file_name)) for file_name in text_files)

def mapfn(k, v):

	def removerPontuacao(w):
		return w.replace('.', '').replace(',', '').replace('\'', '').replace(':', '')

	print 'map ' + k
	from stopwords import allStopWords
	for line in v.splitlines():
		splited = line.split(':::')
		autores = splited[1].split('::')
		titulo = splited[2]
		#print titulo
		#print autores

		words = []
		for word in titulo.split():
			if (word not in allStopWords):
				words.append(removerPontuacao(word))

		for autor in autores:
			yield autor, words

def reducefn(k, v):
	print 'reduce ' + k
	#print v

	words = dict()
	for lista in v:
		for word in lista:
			if word not in words:
				words[word] = 1
			else:
				words[word] += 1


	return words


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
w = csv.writer(open("result.csv", 'w'))
for k, v in results.items():
	w.writerow([k, v])
	
	if k in ['Grzegorz Rozenberg', 'Philip S. Yu', 'Alberto Pettorossi']:

		sortedd = sorted(v.items(), key=operator.itemgetter(1))
		sortedd.reverse()
		i = 0
		words = []
		for word, count in sortedd:
			if i < 2 :
				words.append(word + ': ' + str(count))
				i += 1

		print k + ': ' + str(words)



	if False:
		print('#######################################')
		print('k')
		print(k)
		print('v')
		print(v)

print 'fim'