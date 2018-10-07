import re

output = ""
dictionary = {}
keyword = ["VAR", "AS", "START", "STOP"]
arithmetic_operators = ["(", ")", "*", "/", "%", "+", "-", ">", "<", ">=", "<=", "==", "<>"]
assignment_operators = ["="]
logical_operators = ["AND", "OR", "NOT"]
datatype = ["INT", "CHAR", "BOOL", "FLOAT"]
identifierSyntax = "([_a-zA-Z]+\d*){1,30}"
arithOps_regex = "[\+\-\*\/\%]"
optNegSign = "[\-\+]?"

#TODO sample commit

def cfpl_tokenize(code):
	global output	
	statements = code.split("\n")
	print("From cfpl_tokenize (data: statements): "+repr(statements))
	tokens = list()
	for statement in statements:
		if(statement):			
			content = statement.strip()
			# tag each statement
			tokens.append(getStatementType(content) + ":" + content)
	print("From cfpl_tokenize (data: tokens): "+repr(tokens))
	return tokens

def cfpl_parse(statements):
	# lets scan
	if(isValidStructure(statements)):
		print("From cfpl_parse (data: statements): "+repr(statements))
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
	elif isArithmeticExpression(statement):
		return "ARITH_EXP"
	else:
		return "INVALID"

def isValidStructure(statements):
	global output
	isValid = True
	hasStarted = False
	hasStop = False
	linenumber = 1
	for statement in statements:
		if(re.match("^INVALID", statement)):
			isValid = False		
			output = "Syntax error in line " + repr(linenumber)
			break
		elif(re.match("^VARDEC", statement)):
			if(hasStarted):
				isValid = False
				output = "Invalid variable declaration in line " + repr(linenumber)
				break
			# more work here for VARDEC
			processVarDec(statement)	# <-- this line is out of scope: statement after "break" pls verify is correct
		elif(re.match("^KEYWORD:START$", statement)):
			if(hasStarted):
				isValid = False
				output = "Invalid program structure in line " + repr(linenumber)
				break
			hasStarted = True	# <-- this line is out of scope: statement after "break" pls verify is correct
		elif(re.match("^OUTPUT", statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid program structure in line " + repr(linenumber)
				break
			processoutput(statement)	# <-- this line is out of scope: statement after "break" pls verify is correct
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
	return re.match(identiferSyntax, token)

def isDigit(token):
	return re.match("\d+", token)

def isVarDeclaration(statement):
	# validate variable declaration syntax using regex
	return re.match("^VAR\s"+identifierSyntax+"(=\w+)?(,(\s|)"+identifierSyntax+"(=\w+)?)*\sAS\s(INT|CHAR|BOOL|FLOAT)$", statement)

def isOutput(statement):
	# validate OUTPUT statement syntax using regex
	return re.match('^OUTPUT:\s\w', statement)
	
def processoutput(statement):
	global output
	if(statement):		
		temp = statement.split(' ')[1:] # we don't need the first element
		output = dictionary[temp[0]]

def processVarDec(statement):
	if(statement):
		temp = statement.split(' ')[1:2]
		tokens = temp[0].split(',')
		print("From processVarDec (data: tokens): "+repr(tokens))
		for token in tokens:
			if "=" in token:
				expression = token.split('=')
				identifier = expression[0]
				value = expression[1]
				dictionary.update({identifier:value})
			else:
				dictionary.update({token:''})
		print("From processVarDec (data: dictionary): "+repr(dictionary))
	
def isAssignment(statement):
	return re.match("^"+identifierSyntax+"=(('\w+')|"+identifierSyntax+"|\d|expression)+$", statement); #TODO expression to be identified

def isArithmeticExpression(statement):
	# regex pattern composition:
		# ^								=> start
		# (\-?(\d*\.?\d+)				=> will match: 1, 0.1, .1 (negative or positve)
		# arithOps_regex ([\+\-\*\/\%])	=> single operator only
		# $								=> end

	return re.match("^(\-?(\d*\.?\d+)"+arithOps_regex+"{1}(\-?\d*\.?\d+))+$",statement)

#REGEX SYMBOL GUIDE
# * 	- 0 or more
# \s 	- [ \t\n\r\f\v] -> matches any whitespace
# \S 	- [^ \t\n\r\f\v] -> matches any non-whitespace
# \w    - [_a-zA-Z0-9] matches any alphanumeric
# \W    - [^a-zA-Z0-9_] matches any non-alphanumeric
# \d 	- [0-9] matches number
# ?		- 0 or 1
# +		- 1 or more
# ^		- starts with
# $		- end of regex (grammar)
# {}	- length (min, max) syntax: [pattern]{1,1} -> where [pattern] is grouped
# []	- range of pattern
# ()	- capture group