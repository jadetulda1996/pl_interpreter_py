import re
from . import validate

output = ""
dictionary = {}
isValid = True

def cfpl_tokenize(code):
	global output	
	statements = code.split("\n")
	# print("From cfpl_tokenize (data: statements): "+repr(statements))
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
	validate.clearvarDeclarations()
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
	elif validate.isIFExpression(statement):
		return "IF_EXPR"
	elif validate.isElseExpression(statement):
		return "ELSE_EXPR"
	else:
		return "INVALID"

def parseStatement(statements):
	global output
	global isValid
	hasStarted = False
	hasStop = False
	linenumber = 1
	output = ""
	isValid = True
	hasIfDeclare = False
	hasIfStarted = False
	hasElseDeclare = False
	hasElseStarted = False

	for statement in statements:
		# print(statements[linenumber-1])
		print(linenumber)

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

		# elif(re.match('^KEYWORD:STOP$', statement)):
		# 	if(hasStarted and hasIfDeclare)

		elif(re.match("^OUTPUT", statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid output statement in line " + repr(linenumber)
				break
			#output = ""
			process_output(statement)
			# more work here for OUTPUT

		elif(re.match('^ASSIGNMENT', statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid assignment statement in line " + repr(linenumber)
				break
			process_assignment(statement)
		
		elif(re.match('^IF_EXPR', statement)):
			if(hasStarted == False):
				isValid = False
				output = "Invalid IF statement in line " + repr(linenumber)
				break
			else:
				if(not hasIfDeclare):
					hasIfDeclare = True
					# print('hasIfDeclare: '+repr(hasIfDeclare))
				else:
					isValid = False
					output = "Invalid token 'IF' statement in line " + repr(linenumber)
					break

			output = ""
		
		elif(re.match('^ELSE_EXPR', statement)):
			if(not hasIfDeclare):
				isValid = False
				output = "Invalid ELSE statement in line " + repr(linenumber)
				break
			else:
				if(not hasIfStarted):
					hasIfDeclare = False
					hasElseDeclare = True
					print("if is closed")
					print("else declared")
				else:
					isValid = False
					output = "Expected 'STOP' keyword before else in line " + repr(linenumber)
					break

			output = ""

		elif(hasIfDeclare):
			if(re.match('^KEYWORD:START$', statement)):
				if(hasIfStarted):
					isValid = False
					output = "Invalid token 'START' in line " + repr(linenumber)
					break
				else:
					hasIfStarted = True
					process_controlStructure(statement)
					# print('hasIfStarted: ' + repr(hasIfStarted))

			if(re.match('^KEYWORD:STOP$', statement)):
				print(hasIfStarted)
				if(not hasIfStarted):
					isValid = False
					output = "Expected keyword 'START' in line " + repr(linenumber)
					break
				else:
					hasIfStarted = False

		elif(hasElseDeclare):
			if(re.match('^KEYWORD:START$', statement)):
				if(hasElseStarted):
					isValid = False
					output = "Invalid token 'START' in line " + repr(linenumber)
					break
				else:
					hasElseStarted = True
					print("else started")
					process_controlStructure(statement)


			if(re.match('^KEYWORD:STOP$', statement)):
				if(not hasElseStarted):
					isValid = False
					output = "Expected keyword 'START' in line " + repr(linenumber)
					break
				else:
					hasElseStarted = False
					hasElseDeclare = False
			
		elif(re.match('^KEYWORD:START$', statement)):
			if(hasStarted == True):
				isValid = False
				output = "Invalid 'START' statement in line " + repr(linenumber)
				break

			hasStarted = True

		if not isValid: # insert "elif" above this line
			output += "\nError was found in line : " + repr(linenumber)
			break

		linenumber += 1

def process_output(statement):
	global output
	global dictionary
	global isValid
	if(statement):
		temp = re.sub("OUTPUT:", "", statement).strip()
		if temp in dictionary.keys():
			output = dictionary[temp]
		else:
			output = "Error : Unspecified variable : " + repr(temp)
			isValid = False

def process_vardec(statement):
	global dictionary
	if(statement):
		# remove specified text from the string instead of using split
		temp = re.sub("VARDEC:VAR|AS|INT|CHAR|BOOL|FLOAT", "", statement).strip()
		# now only relevant text remains, lets split
		tokens = temp.split(',')
		# print("From processVarDec (data: tokens): "+repr(tokens))
		for token in tokens:
			if "=" in token:
				expression = token.split('=')
				identifier = expression[0].strip()
				value = expression[1].strip()
				dictionary[identifier] = value
			else:
				dictionary[token.strip()] = validate.getDefaultValue(statement.split(' ')[-1])
		# print(temp)
		#print("Dictionary content after process_vardec : " + repr(dictionary))

def process_assignment(statement):
	global output
	global dictionary
	global isValid
	if(statement):
		temp = re.sub("ASSIGNMENT:", "", statement).strip()
		tokens = temp.split('=')
		value = tokens[-1].strip() # element after the '=' operator
		
		if(validate.isIdentifier(value)):
			if value in dictionary.keys():
				value = dictionary[value]			
			else:
				output = "Error : Undefined variable : " + repr(value)
				isValid = False
		
		if(isValid):
			for token in tokens[:-1]:
				identifier = token.strip()
				if identifier in dictionary.keys():
					dictionary[identifier] = value
				else:
					output = "Error : Undefined variable : " + repr(identifier)
					isValid = False
					break
		print("Dictionary content after process_assignment : " + repr(dictionary))

def process_controlStructure(statement):
	return True

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