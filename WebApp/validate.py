import re

keyword = ["VAR", "AS", "START", "STOP"]
arithmetic_operators = ["(", ")", "*", "/", "%", "+", "-", ">", "<", ">=", "<=", "==", "<>"]
assignment_operators = ["="]
logical_operators = ["AND", "OR", "NOT"]
datatype = ["INT", "CHAR", "BOOL", "FLOAT"]
identifierSyntax = "(_?[a-zA-Z]+\d*){1,30}" #<-- "_" should be followed by a letter
arithOps_regex = "[\+\-\*\/\%]"
number = "(\-?\d*\.?\d+)"
boolOps = "(\>|\<|(\>\=)|(\<\=)|(\=\=)|(\<\>))"
logicOps = "(AND|OR|NOT)"

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

def isOutput(statement):
	# validate OUTPUT statement syntax using regex
	return re.match('^OUTPUT:\s\w', statement)

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
	return re.match(identifierSyntax, token)

def isInteger32(token):
	if(re.search("\.", token)):
		return False

	if(abs(int(token)) > (2**31-1)):
		return False

	return re.match("\-?\d+", token)

def isFloat(token):
	return re.match("\-?\d*\.\d+", token)

def isChar(token):
	if(isinstance(token, str)):
		return re.match("\'\w?\.?\'", token)

	return False

def isBool(token):
	return re.match("^(TRUE|FALSE)$", token)

def getVarValue(token):
	return token.split("=",1)[1].strip()

def getVarIdentifier(token):
	return token.split("=",1)[0].strip()

def isVarDeclaration(statement):
	varDeclarations = {}
	# remove specified text from the string instead of using split
	temp = re.sub("VAR|AS|INT|CHAR|BOOL|FLOAT", "", statement).strip()
	varType = re.split("\s+", statement)[::-1][0] #[::-1] -> reverse list, [0] -> get varType
	identifierTokens = []

	if(re.search(",", temp)):
		identifierTokens = temp.split(",") #split multiple declared identifiers
	else:
		identifierTokens.append(temp) #single identifier declared
	
	if(identifierTokens):
		for varToken in identifierTokens:
			value = ""
			identifier = ""
			if(re.search("=", varToken)): #get the value
				identifier = getVarIdentifier(varToken)
				value = getVarValue(varToken)

				if(isMatchValueVarDecType(value, varType)):
					varDeclarations[identifier] = value
				else:
					return False

			else:
				varDeclarations[varToken] = ''

	allowedData		= "(\-?\d+|\-?\d*\.\d+|\'\w?\.?\'|TRUE|FALSE)"
	requiredDec 	= "VAR\s"+identifierSyntax
	optDec			= "(\s*=\s*"+allowedData+")?(\s*,\s*"+identifierSyntax+"(\s*=\s*"+allowedData+")?)*\s"
	varDec 			= requiredDec+optDec
	varType			= "AS\s(INT|CHAR|BOOL|FLOAT)"
	regPattern = "^"+varDec+varType+"$"
	
	return re.match(regPattern, statement)

def isMatchValueVarDecType(value, typeUsed):
	if(re.match("INT", typeUsed)):
		return isInteger32(value)
	elif(re.match("CHAR", typeUsed)):
		return isChar(value)
	elif(re.match("BOOL", typeUsed)):
		return isBool(value)
	elif(re.match("FLOAT", typeUsed)):
		return isFloat(value)
	else:
		return re.match("(INT|FLOAT|CHAR|BOOL)", typeUsed)

def isAssignment(statement):

	#To get the value of the identifier to be validated
	temp = statement

	if(re.search("=",temp)):
		value = temp.split("=", 1)[1] # remove identifier and its first "=" occurence

		if(isArithmeticExp(value)):
			return True
		elif(isBoolean(value)):
			return True

		allowedData 			= "('\w+')|"+identifierSyntax+"|"+number+"|"
		firstAssignment			= identifierSyntax+"\s*={1}\s*("+allowedData+")"
		addtnAssignment_opt		= "("+identifierSyntax+"={1}("+allowedData+"))*"
		regPattern				= "^"+firstAssignment+addtnAssignment_opt+"$"
		return re.match(regPattern,statement)
	else:
		return False

	#Note: Check variable declaration on top (in process_assignment function)

	#sample data:
		# 1=1 or '1'=1 or 1=a		=> error: can't assign value to a non-identifier
		# a=1 or a=a or a=-1		=> success: identifier = data(+ or -) or identifier
		# a==a 						=> error: is not an assignment operator

def isExpression(statement):
	return re.match(regPattern,statement)

def isArithmeticExp(statement):
	digitOrIdentifer	= "("+identifierSyntax+"|"+number+")"
	ops 				= arithOps_regex+"{1}"
	firstExp			= digitOrIdentifer+ops+digitOrIdentifer
	addtnExp_opt		= "("+ops+digitOrIdentifer+")*"
	regPattern			= "^"+firstExp+addtnExp_opt+"$"
	return re.match(regPattern,statement)

def isBooleanExp(statement):
	allowedData					= "("+identifierSyntax+"|"+number+")"
	singleBoolExp				= "("+allowedData+"\s?"+boolOps+"\s?"+allowedData+")"
	addtnBoolExp_opt			= "("+boolOps+allowedData+")*"
	multiBoolExp				= "("+singleBoolExp+addtnBoolExp_opt+")"
	regPattern					= "^("+multiBoolExp+")$"
	return re.match(regPattern,statement)

def isBoolean(statement):
	if(re.search(logicOps, statement)):
		allowedData					= "("+identifierSyntax+"|"+number+")"
		singleBoolOpr				= "("+allowedData+"\s"+logicOps+"\s"+allowedData+")"
		addtnBoolOpr_opt			= "(\s"+logicOps+"\s"+allowedData+")*"
		multiBoolOpr				= "("+singleBoolOpr+addtnBoolOpr_opt+")"
		regPattern					= "^("+multiBoolOpr+")$"
		return re.match(regPattern,statement)

	else:
		return isBooleanExp(statement)
	# regex pattern composition:
		# ^								=> start
		# (\-?(\d*\.?\d+)				=> will match: 1, 0.1, .1 (negative or positve)
		# arithOps_regex ([\+\-\*\/\%])	=> single operator only
		# $								=> end

	# sample data:
		# 1+a10.			=> error: has "." on last statement
		# -1+-1				=> success: negative + negative
		# 0.1-1				=> success: (+)decimal - (+)
		# a+1 or 1+a		=> success: identifier + number (and vice versa)
		# a+2+4+1--0.1		=> success: can detect multiple operation