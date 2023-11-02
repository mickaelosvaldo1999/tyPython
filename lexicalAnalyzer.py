# Analyzes the input file and returns a list of tokens and lexemes
class scanner():
    def __init__(self,file):
        with open(file, "r") as file:
            scan = file.readlines()
            for i in range(len(scan)):
                scan[i] = scan[i].strip("\n")
                
            print (scan)
    
    #Using default python functions to analyze the input
    def __isDigit(self, char):
        return char.isdigit()
    
    def __isCharUpper(self, char: chr):
        return char.isupper()

    def _isCharLower(self, char: chr):
        return char >= 'a' and char <= 'z'

    def _isSymbol(self, char: chr):
        return char == '(' or char == ')' or char == '#' or char == "[" or char == "]"

    def _isOperator(self, char: chr):
        return char == '+' or char == '-' or char == '*'
                