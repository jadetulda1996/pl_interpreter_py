import re
from . import validate
from . import constant

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

	print(statements[-1])

	for statement in statements:

		if not (re.match('^KEYWORD:STOP$', statements[-1])):
			isValid = False
			output = "Invalid end of program."
			break

		elif(re.match("^INVALID", statement)):
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
					output = ""
					process_controlStructure(statement)
					hasIfDeclare = True
				else:
					isValid = False
					output = "Invalid token 'IF' statement in line " + repr(linenumber)
					break
		
		elif(re.match('^ELSE_EXPR', statement)):
			if(not hasIfDeclare):
				isValid = False 
				output = "Invalid ELSE statement in line " + repr(linenumber)
				break
			else:
				if(not hasIfStarted):
					hasIfDeclare = False
					hasElseDeclare = True
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

			if(re.match('^KEYWORD:STOP$', statement)):
				if(not hasIfStarted):
					isValid = False
					output = "Expected keyword 'START' in line " + repr(linenumber)
					break
				else:
					hasIfStarted = False

					try:
						if(not re.match('^ELSE_EXPR', statements[linenumber])):
							hasIfDeclare = False
					except Exception as e:
						isValid = False
						output = "Expected keyword 'STOP' in line " + repr(linenumber)
						break

		elif(hasElseDeclare):
			if(re.match('^KEYWORD:START$', statement)):
				if(hasElseStarted):
					isValid = False
					output = "Invalid token 'START' in line " + repr(linenumber)
					break
				else:
					hasElseStarted = True
					print("just here")


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
		tokens = temp.split('&')
		print("from output")
		print(tokens)
		for token in tokens:
			value = token.strip()
			if validate.isIdentifier(value):
				identifier = value
				if identifier in dictionary.keys():
					output += dictionary[identifier]
				else:
					output = "Error : Unspecified variable : " + repr(temp)
					isValid = False
					break
			else:
				output += value + "\ntest"

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
				dictionary[identifier] = value.replace("\'","")
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
		elif(validate.isArithmeticExp(value)):
			value = eval(value)
		
		if(isValid):
			for token in tokens[:-1]:
				identifier = token.strip()
				if identifier in dictionary.keys():
					dictionary[identifier] = str(value).replace("\'","")
				else:
					output = "Error : Undefined variable : " + repr(identifier)
					isValid = False
					break
		print("Dictionary content after process_assignment : " + repr(dictionary))

def process_controlStructure(statement):
	global output
	global isValid
	opsUsed = []
	result = True

	boolOps = constant.getBoolOps()
	logicOps = constant.getLogicOps()

	boolExp = validate.getIF_expr_Param(statement, 2)
	ifParamIdentifiers = re.split("\s["+boolOps+"|"+logicOps+"]*\s", boolExp)
	boolOps_Used = re.split("\s", boolExp)

	for ops in boolOps_Used:							# <-- get operator used
		if(re.match(boolOps+"|"+logicOps, ops)):
			opsUsed.append(ops)

	for param in ifParamIdentifiers:					# <-- check if identifier exists
		if(not checkIfParamIdentifier(param)):
			print("from here")
			output = "Error : Undefined variable : " + repr(param)
			isValid = False
			break
		else:
			if(dictionary[param] == "FALSE" or dictionary[param] == False):
				dictionary[param] = False
			else:
				dictionary[param] = True

	# print(dictionary)
	for index in range(0, len(opsUsed)):	#range(start, iterations)
		if(index == 0):
			if(opsUsed[index] == "AND"):
				print(dictionary[ifParamIdentifiers[index]])
				print(dictionary[ifParamIdentifiers[index+1]])
				result = (dictionary[ifParamIdentifiers[index]] and dictionary[ifParamIdentifiers[index+1]])
				print(str(index+1) + " iteration: " + repr(result))

			elif(opsUsed[index] == "OR"):
				result = (dictionary[ifParamIdentifiers[index]] or dictionary[ifParamIdentifiers[index+1]])
				print(str(index+1) + " iteration: " + repr(result))

			if(not result):
				print(False)
				break

		elif(index > 0):
			if(opsUsed[index] == "AND"):
				result = (result and dictionary[ifParamIdentifiers[index+1]])
				print(str(index+1) + " iteration: " + repr(result))
				
			elif(opsUsed[index] == "OR"):
				result = (result or dictionary[ifParamIdentifiers[index+1]])
				print(str(index+1) + " iteration: " + repr(result))

			if(not result):
				print(False)
				break


def checkIfParamIdentifier(param):
	if param in dictionary.keys():
		return True

	return False