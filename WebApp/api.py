import re
from . import validate

output = ""
dictionary = {}

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
	if(parseStatement(statements)):
		print("From cfpl_parse (data: statements): "+repr(statements))
		# TODO traverse the statement and work on OUTPUT statement
	return output

def getStatementType(statement):
	if validate.isComment(statement):
		return "COMMENT"
	elif validate.isKeyword(statement):
		return "KEYWORD"
	elif validate.isVarDeclaration(statement):
		return "VARDEC"
	elif validate.isOutput(statement):
		return "OUTPUT"
	elif validate.isAssignment(statement):
		return "ASSIGNMENT"
	elif validate.isArithmeticExpression(statement):
		return "ARITH_EXP"
	else:
		return "INVALID"

def parseStatement(statements):
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
			process_vardec(statement)
			if(hasStarted):
				isValid = False
				output = "Invalid start statement in line " + repr(linenumber)
				break
		elif(re.match('^KEYWORD:START$', statement)):
			hasStarted = True	# <-- this line is out of scope: statement after "break" pls verify is correct
			continue
		elif(re.match("^OUTPUT", statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid output statement in line " + repr(linenumber)
				break
			process_output(statement)
			# more work here for OUTPUT
		elif(re.match('^ASSIGNMENT', statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid assignment statement in line " + repr(linenumber)
				break
			process_assignment(statement) # <-- (this is correct) this line is out of scope: statement after "break" pls verify is correct
		
		linenumber += 1
	return isValid

def process_output(statement):
	global output	
	if(statement):		
		temp = statement.split(' ')[1:] # we don't need the first element
		output = dictionary[temp[0]]
		
def process_vardec(statement):
	global dictionary
	if(statement):
		temp = statement.split(' ')[1:2]
		tokens = temp[0].split(',')
		print("From processVarDec (data: tokens): "+repr(tokens))
		for token in tokens:
			if "=" in token:
				expression = token.split('=')
				identifier = expression[0]
				value = expression[1]
				dictionary[identifier] = value
			else:
				dictionary[token] = ''
		print(dictionary)

def process_assignment(statement):	
	global dictionary
	if(statement):
		temp = statement.split('ASSIGNMENT:')[1:] #remove assignment tag
		tokens = temp[0].split('=')
		identifier = tokens[0].strip() # element before the '=' operation
		value = tokens[1].strip() # element after the '=' operator
		dictionary[identifier] = value
		print(dictionary)


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