import re

output = ""
dictionary = {}
keyword = ["VAR", "AS", "START", "STOP"]
arithmetic_operators = ["(", ")", "*", "/", "%", "+", "-", ">", "<", ">=", "<=", "==", "<>"]
assignment_operators = ["="]
logical_operators = ["AND", "OR", "NOT"]
datatype = ["INT", "CHAR", "BOOL", "FLOAT"]
identifierSyntax = "([_a-zA-Z]+[0-9]*){1,30}"

#TODO sample commit

def cfpl_tokenize(code):
	global output	
	statements = code.split("\n")
	print(statements)
	tokens = list()
	for statement in statements:
		if(statement):			
			content = statement.strip()
			# tag each statement
			tokens.append(getStatementType(content) + ":" + content)
	print(tokens)
	return tokens

def cfpl_parse(statements):
	# lets scan
	if(isValidStructure(statements)):
		print(statements)
		# TODO traverse the statement and work on OUTPUT statement
	return output

def getStatementType(statement):
	if isComment(statement):
		return "COMMENT"
	elif isKeyword(statement):
		return "KEYWORD"
	elif isVarDeclaration(statement):
		return "VARDEC"
	elif isOutput(statement):
		return "OUTPUT"
	elif isAssignment(statement):
		return "ASSIGNMENT"
	else:
		return "INVALID"

def isValidStructure(statements):
	global output
	isValid = True
	hasStarted = False
	hasStop = False
	linenumber = 1
	for statement in statements:
		if(re.match('^INVALID', statement)):
			isValid = False		
			output = "Syntax error in line " + repr(linenumber)
			break
		elif(re.match("^VARDEC", statement)):
			if(hasStarted):
				isValid = False
				output = "Invalid variable declaration in line " + repr(linenumber)
				break
			# more work here for VARDEC
			processVarDec(statement)
		elif(re.match('^KEYWORD:START$', statement)):
			if(hasStarted):
				isValid = False
				output = "Invalid program structure in line " + repr(linenumber)
				break
			hasStarted = True
		elif(re.match('^OUTPUT', statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid program structure in line " + repr(linenumber)
				break
			processoutput(statement)
			# more work here for OUTPUT
		linenumber += 1
	return isValid


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

def isComment(statement):
	# returns: COMMENT
	return re.match("^\*",statement)

def isKeyword(token):
	#return token in keyword
	return re.match("^(VAR|AS|START|STOP)$", token)

def isDatatype(token):
	return token in datatype

def isAssignmentOperator(token):
	return token in assignment_operators

def isArithmeticOperator(token):
	return token in arithmetic_operators

def isIdentifier(token):
	# return re.match("[_a-zA-Z][_a-zA-Z0-9]{0,30}", token)
	return re.match(identiferSyntax, token)

def isDigit(token):
	return re.match("\d+", token)

def isVarDeclaration(statement):
	# validate variable declaration syntax using regex
	return re.match("^VAR\s"+identifierSyntax+"(=[_a-zA-Z0-9]+)(,(\s|)"+identifierSyntax+"(=[_a-zA-Z0-9]+)?)*\sAS\s(INT|CHAR|BOOL|FLOAT)$", statement)

def isOutput(statement):
	# validate OUTPUT statement syntax using regex
	return re.match('^OUTPUT:\s[_a-zA-Z0-9]', statement)
	
def processoutput(statement):
	global output	
	if(statement):		
		temp = statement.split(' ')[1:] # we don't need the first element
		output = dictionary[temp[0]]

def processVarDec(statement):
	if(statement):
		temp = statement.split(' ')[1:2]
		tokens = temp[0].split(',')
		print(tokens)
		for token in tokens:
			if "=" in token:
				expression = token.split('=')
				identifier = expression[0]
				value = expression[1]
				dictionary.update({identifier:value})
			else:
				dictionary.update({token:''})
		print(dictionary)
	
def isAssignment(statement):
	return re.match("^"+identifierSyntax+"(\s|)={1,1}(\s|)(('[_a-zA-Z0-9]*')|"+identifierSyntax+"|[0-9]|expression)+$", statement); #TODO expression to be identified

#valid grammar for expression
	#arithmetic = number to number relationship | identifier (int | float) to number (vice versa) |
	#

#REGEX SYMBOL GUIDE
# * 	- 0 or more
# \s 	- space
# ?		- 0 or 1
# +		- 1 or more
# ^		- starts with
# $		- end of regex (grammar)
# {}	- length (min, max) syntax: [pattern]{1,1} -> where [pattern] is grouped
# []	- range of pattern
# ()	- capture group