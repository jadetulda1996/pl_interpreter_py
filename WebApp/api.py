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
	dictionary.clear()
	parseStatement(statements)
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
				
			output = ""

		elif(re.match('^KEYWORD:START$', statement)):
			hasStarted = True

		elif(re.match("^OUTPUT", statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid output statement in line " + repr(linenumber)
				break
				
			output = ""
			process_output(statement)
			# more work here for OUTPUT

		elif(re.match('^ASSIGNMENT', statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid assignment statement in line " + repr(linenumber)
				break
				
			output = ""
			process_assignment(statement)

		linenumber += 1
	return isValid

def process_output(statement):
	global output
	global dictionary	
	if(statement):		
		temp = re.sub("OUTPUT:", "", statement).strip()
		if temp in dictionary.keys():
			output = dictionary[temp]
		else:
			output = "Error : Unspecified variable : " + repr(temp)

def process_vardec(statement):
	global dictionary
	if(statement):	
		# remove specified text from the string instead of using split
		temp = re.sub("VARDEC:VAR|AS|INT|CHAR|BOOL|FLOAT", "", statement).strip()
		# now only relevant text remains, lets split
		tokens = temp.split(',')
		print("From processVarDec (data: tokens): "+repr(tokens))
		for token in tokens:
			if "=" in token:
				expression = token.split('=')
				identifier = expression[0].strip()
				value = expression[1].strip()
				dictionary[identifier] = value
			else:
				dictionary[token] = ''
		print(temp)
		print("Dictionary content after process_vardec : " + repr(dictionary))

def process_assignment(statement):	
	global output
	global dictionary
	if(statement):
		#temp = statement.split('ASSIGNMENT:')[1:] #remove assignment tag
		temp = re.sub("ASSIGNMENT:", "", statement).strip()
		tokens = temp.split('=')
		identifier = tokens[0].strip() # element before the '=' operation
		value = tokens[1].strip() # element after the '=' operator
		if identifier in dictionary.keys():
			dictionary[identifier] = value
		else:
			output = "Error : Unspecified variable : " + repr(identifier)

		print("Dictionary content after process_assignment : " + repr(dictionary))


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