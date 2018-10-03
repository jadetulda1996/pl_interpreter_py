import re

reserved = ['VAR', 'OUTPUT', 'INPUT', 'AS']
ar_operators = ['(', ')', '*', '/', '%', '+', '-', '>', '<', '>=', '<=', '==', '<>']
as_operators = ['=']
datatype = ['INT', 'CHAR', 'BOOL', 'FLOAT']

def cfpl_tokenize(code):
	from nltk.tokenize import word_tokenize
	tokens = word_tokenize(code)
	#code = code.replace('\n', ' NEWLINE ')
	#tokens = code.split(' ')
	print(tokens)
	return tokens

def cfpl_lexer(tokens):
	lextoken = list()
	for token in tokens:
		lextoken.append(checkTokenType(token) + ":" + token)
	print(lextoken)
	return "verify console output for now..."

def cfpl_parser(lextoken):
	return "parser..."

def checkTokenType(token):
	tokentype = ""
	if token in reserved:
		tokentype = "RESERVED"
	elif token in datatype:
		tokentype = "DATATYPE"
	elif token in as_operators:
		tokentype = "AS_OPERATOR"
	elif token in ar_operators:
		tokentype = "AR_OPERATOR"
	elif isIdentifier(token):
		tokentype = "INDENTIFIER"
	elif isDigit(token):
		tokentype = "DIGIT"	
	else:
		tokentype = "INVALID"

	return tokentype

def isIdentifier(token):
	return re.search('[_a-zA-Z][_a-zA-Z0-9]{0,30}', token)

def isDigit(token):
	return re.search('\d+', token)