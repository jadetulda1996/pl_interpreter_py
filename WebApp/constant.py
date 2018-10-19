identifierSyntax = "(_?[a-zA-Z_]+\d*){1,30}" #<-- "_" should be followed by a letter
arithOps_regex = "[\+\-\*\/\%]"
number = "(\-?\d*\.?\d+)"
boolOps = "((\>\=)|(\<\=)|(\=\=)|(\<\>)|\>|\<)"
logicOps = "(AND|OR|NOT)"

def getIdentifierSyntax():
    return identifierSyntax

def getArithOps_Regex():
    return arithOps_regex

def getNumber():
    return number

def getBoolOps():
    return boolOps

def getLogicOps():
    return logicOps




#REGEX SYMBOL GUIDE
# *     - 0 or more
# \s    - [ \t\n\r\f\v] -> matches any whitespace
# \S    - [^ \t\n\r\f\v] -> matches any non-whitespace
# \w    - [_a-zA-Z0-9] matches any alphanumeric
# \W    - [^a-zA-Z0-9_] matches any non-alphanumeric
# \d    - [0-9] matches number
# ?     - 0 or 1
# +     - 1 or more
# ^     - starts with
# $     - end of regex (grammar)
# {}    - length (min, max) syntax: [pattern]{1,1} -> where [pattern] is grouped
# []    - range of pattern
# ()    - capture group