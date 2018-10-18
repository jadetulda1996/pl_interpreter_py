import re
from . import constant

keyword = ["VAR", "AS", "START", "STOP"]
arithmetic_operators = ["(", ")", "*", "/", "%", "+", "-", ">", "<", ">=", "<=", "==", "<>"]
assignment_operators = ["="]
logical_operators = ["AND", "OR", "NOT"]
datatype = ["INT", "CHAR", "BOOL", "FLOAT"]
varDeclarations = {}

identifierSyntax = constant.getIdentifierSyntax()
arithOps_regex = constant.getArithOps_Regex()
number = constant.getNumber()
boolOps = constant.getBoolOps()
logicOps = constant.getLogicOps()


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
	return re.match('^OUTPUT:\s(\w|#)', statement)

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

	return re.match("\-?\d+", token)

	if(abs(int(token)) > (2**31-1)):
		return False

def isFloat(token):
	return re.match("\-?\d*(\.\d+)?", token)

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
	global varDeclarations
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

				if(identifier in varDeclarations):
					return False

				if(isMatchValueVarDecType(value, varType)):
					varDeclarations[identifier] = value
				else:
					return False

			else:
				identifier = varToken

				if(identifier in varDeclarations):
					return False
				else:
					varDeclarations[identifier] = getDefaultValue(varType)

	allowedData		= "(\-?\d+|\-?\d*(\.\d+)?|\'\w?\.?\'|TRUE|FALSE)"
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

def getDefaultValue(typeUsed):
	if(re.match("(INT|FLOAT)", typeUsed)):
		return 0
	elif(re.match("CHAR", typeUsed)):
		return ""
	elif(re.match("BOOL", typeUsed)):
		return "FALSE"

def isAssignment(statement):

	#To get the value of the identifier to be validated
	temp = statement

	if(re.search("=",temp) and not re.search("IF",temp)):
		value = temp.split("=", 1)[1] # remove identifier and its first "=" occurence

		if(isArithmeticExp(value.strip())):
			return True
		elif(isBoolean(value.strip())):
			return True

		allowedData 			= "('\w+')|"+identifierSyntax+"|"+number+"|"
		firstAssignment			= identifierSyntax+"\s?={1}\s?("+allowedData+")"
		addtnAssignment_opt		= "("+identifierSyntax+"={1}("+allowedData+"))*"
		regPattern				= "^"+firstAssignment+addtnAssignment_opt+"$"
		return re.match(regPattern,statement)
	else:
		return False

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
	addtnBoolExp_opt			= "(\s?"+boolOps+"\s?"+allowedData+")*"
	multiBoolExp				= "("+singleBoolExp+addtnBoolExp_opt+")"
	regPattern					= "^("+multiBoolExp+")$"

	return re.match(regPattern,statement)

def isBoolean(statement):
	if(re.search(logicOps, statement)):
		allowedData					= "("+identifierSyntax+"|"+number+")"
		singleBoolOpr				= "("+allowedData+"\s?"+logicOps+"\s"+allowedData+")"
		addtnBoolOpr_opt			= "(\s?"+logicOps+"\s?"+allowedData+")*"
		multiBoolOpr				= "("+singleBoolOpr+addtnBoolOpr_opt+")"
		regPattern					= "^("+multiBoolOpr+")$"

		return re.match(regPattern,statement)

	else:
		return isBooleanExp(statement)

def clearvarDeclarations():
	varDeclarations.clear()

def isIFExpression(statement):
	boolExp = getIF_expr_Param(statement, 1)

	ifSyntax = re.sub("[^(IF\s?\(|\s*|\)$)]*", "", statement)
	ifsynt = re.sub("\s*", "", ifSyntax)
	
	isBoolExpr = isBoolean(boolExp)

	if(isBoolExpr):
		return re.match("^IF\s?\(\)$", ifsynt)
	else:
		return False

def isElseExpression(statement):
	return re.match('^ELSE$', statement)

def getIF_expr_Param(statement, flag): #flag means where the request comes from
	if(flag == 1): #means inside request
		return re.sub("^IF\s?\(|\)$", "", statement)
	else:
		return re.sub("^IF_EXPR:IF\s?\(|\)$", "", statement)