import re

keyword = ['VAR', 'OUTPUT:', 'INPUT:', 'AS', 'START', 'STOP']
arithmetic_operators = ['(', ')', '*', '/', '%', '+', '-', '>', '<', '>=', '<=', '==', '<>']
assignment_operators = ['=']
logical_operators = ['AND', 'OR', 'NOT']
datatype = ['INT', 'CHAR', 'BOOL', 'FLOAT']

def cfpl_tokenize(code):
	#from nltk.tokenize import word_tokenize
	#tokens = word_tokenize(code)
	#code = code.replace('\n', ' NEWLINE ')
	statements = code.split('\n')
	#tokens = re.split(' |\n', code)
	tokens = list()
	for statement in statements:
		#filter all empty elements in the array
		#filtered = filter(None, statement.split(' ')) 
		#tokens = cfpl_lexer(filtered)
		#print(tokens)
		content = statement.strip()
		tokens.append(checkStatementType(content) + ':' + content)
	print(tokens)
	return "on testing"

def cfpl_lexer(tokens):
	lextoken = list()
	for token in tokens:
		lextoken.append(checkTokenType(token) + ":" + token)
	return lextoken 

def cfpl_parse(statements):
	return "check console for now..."

def checkStatementType(statement):
	if isComment(statement):
		return 'COMMENT'
	elif statement == 'START':
		return 'START'
	elif statement == 'STOP':
		return 'STOP'
	elif isVarDeclaration(statement):
		return 'VARDEC'
	else:
		return 'INVALID'

def isComment(statement):
	return True if statement[0][0] == '*' else False

def isVarDeclaration(statement):
	tokens = statement.split(' ')
	if tokens[0] == 'VAR':
		return True

def checkTokenType(token):
	tokentype = ""
	if token in keyword:
		tokentype = "KEYWORD"
	elif token in datatype:
		tokentype = "DATATYPE"
	elif token in assignment_operators:
		tokentype = "ASSIGNMENT_OPS"
	elif token in arithmetic_operators:
		tokentype = "ARITHMETIC_OPS"
	elif token == '\n':
		tokentype = "NEWLINE"
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

