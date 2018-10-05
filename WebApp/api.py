import re

keyword = ['VAR', 'OUTPUT:', 'INPUT:', 'AS', 'START', 'STOP']
arithmetic_operators = ['(', ')', '*', '/', '%', '+', '-', '>', '<', '>=', '<=', '==', '<>']
assignment_operators = ['=']
logical_operators = ['AND', 'OR', 'NOT']
datatype = ['INT', 'CHAR', 'BOOL', 'FLOAT']

def cfpl_tokenize(code):	
	statements = code.split('\n')
	tokens = list()
	for statement in statements:
		if(statement):			
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
	elif isKeyword(statement):
		return 'KEYWORD'
	elif isVarDeclaration(statement):
		return 'VARDEC'
	else:
		return 'INVALID'

def isComment(statement):
	return True if statement[0][0] == '*' else False

def checkTokenType(token):
	tokentype = ""
	if isKeyword(token):
		tokentype = "KEYWORD"
	elif isDatatype(token):
		tokentype = "DATATYPE"
	elif isAssignmentOperator(token):
		tokentype = "ASSIGNMENT_OPS"
	elif isArithmeticOperator(token):
		tokentype = "ARITHMETIC_OPS"
	elif isIdentifier(token):
		tokentype = "INDENTIFIER"
	elif isDigit(token):
		tokentype = "DIGIT"	
	else:
		tokentype = "INVALID"

	return tokentype

def isKeyword(token):
	return token in keyword

def isDatatype(token):
	return token in datatype

def isAssignmentOperator(token):
	return token in assignment_operators

def isArithmeticOperator(token):
	return token in arithmetic_operators

def isIdentifier(token):
	return re.match('[_a-zA-Z][_a-zA-Z0-9]{0,30}', token)

def isDigit(token):
	return re.match('\d+', token)

def isVarDeclaration(statement):
	# attempt to use regex to validate variable declaration syntax
	return re.match('^VAR\s[_a-zA-Z]+[0-9]*(=[_a-zA-Z0-9])?(,[_a-zA-Z0-9](=[_a-zA-Z0-9])?)*\sAS\s(INT|CHAR|BOOL|FLOAT)$', statement)

def isVarDeclaration_xxx(statement):
	tokens = statement.split(' ')
	if tokens[0] == 'VAR':
		if tokens[-1] in datatype:
			if isIdentifier(tokens[1]):
				return True
