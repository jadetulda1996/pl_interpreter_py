import re

keyword = ["VAR", "AS", "START", "STOP"]
arithmetic_operators = ["(", ")", "*", "/", "%", "+", "-", ">", "<", ">=", "<=", "==", "<>"]
assignment_operators = ["="]
logical_operators = ["AND", "OR", "NOT"]
datatype = ["INT", "CHAR", "BOOL", "FLOAT"]
identifierSyntax = "([_a-zA-Z]+\d*){1,30}"
arithOps_regex = "[\+\-\*\/\%]"
number = "(\-?\d*\.?\d+)"

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

def isDigit(token):
	return re.match("\d+", token)

def isVarDeclaration(statement):
	# allow spaces between identifiers and/or its values
	requiredDec 	= "VAR\s"+identifierSyntax
	optDec			= "(\s*=\s*\w+)?(\s*,\s*"+identifierSyntax+"(\s*=\s*\w+)?)*\s"
	varDec 			= requiredDec+optDec
	varType			= "AS\s(INT|CHAR|BOOL|FLOAT)"
	regPattern = "^"+varDec+varType+"$"
	
	return re.match(regPattern, statement)

def isAssignment(statement):
	temp = statement
	tokens = temp.split('=')
	identifier = tokens[0].strip() # element before the '=' operation
	value = tokens[1].strip() # element after the '=' operator
	
	if(isArithmeticExpression(value)):
		return True

	allowedData 			= "('\w+')|"+identifierSyntax+"|"+number+"|"
	firstAssignment			= identifierSyntax+"\s*={1}\s*("+allowedData+")"
	addtnAssignment_opt		= "(={1}("+allowedData+"))*"
	regPattern				= "^"+firstAssignment+addtnAssignment_opt+"$"
	return re.match(regPattern,statement)
	#TODO fix bug (for multiple assignment, "=" must only followed to an identifier)

	#Note: Check variable declaration on top (in process_assignment function)

	#sample data:
		# 1=1 or '1'=1 or 1=a		=> error: can't assign value to a non-identifier
		# a=1 or a=a or a=-1		=> success: identifier = data(+ or -) or identifier
		# a==a 						=> error: is not an assignment operator

def isArithmeticExpression(statement):
	print("statement from isAssignment: "+repr(statement))
	digitOrIdentifer	= "("+identifierSyntax+"|"+number+")"
	ops 				= arithOps_regex+"{1}"
	firstExp			= digitOrIdentifer+ops+digitOrIdentifer
	addtnExp_opt		= "("+ops+digitOrIdentifer+")*"
	regPattern			= "^"+firstExp+addtnExp_opt+"$"

	# print(re.match(regPattern,statement))
	return re.match(regPattern,statement)


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