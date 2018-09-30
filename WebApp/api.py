
def cfpl_tokenize(msg):
	from nltk.tokenize import word_tokenize
	tokens = word_tokenize(msg)
	return tokens

def cfpl_lexer(msg):    
	str =  msg[0] + " from lexer"
	return str

def cfpl_parser(msg):
	return "parser..."