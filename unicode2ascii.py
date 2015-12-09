import unicodedata

def unicode2ascii(data):
	return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')

data = u'\u005f\u0066\u0061\u006e\u0073\u007d'
print unicode2ascii(data)