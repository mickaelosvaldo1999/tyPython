from tokens import Token
# Analyzes the input file and returns a list of tokens and lexemes
class scanner():
    def __init__(self,file):
        with open(file, "r") as file:
            scan = file.readlines()
            
            #verifying if the file is empty
            if not scan:
                raise Exception("Lexical analyzer: Empty file")
            
            #removing spaces and \n in the end of the line
            scan = [line.rstrip() for line in scan]
                    
            #removing empty lines
            scan = [x for x in scan if x]
            
            #removing comments
            scan = [line for line in scan if not line.lstrip().startswith('$')]
                
            #removing tabs
            scan = [line.lstrip() for line in scan]
                
            print(scan)
            
            #Splitting the lines into lexemes
            for i,line in enumerate(scan):
                scan[i] = line.split(" ")
                for j,word in enumerate(scan[i]):
                    scan[i][j] = self.readToken(word,i)
            
            print(scan[0][0])
            
    
    #Using default python functions to analyze the input
    def __isDigit(self, char):
        return char.isdigit()
    
    def __isCharUpper(self, char: chr):
        return char.isupper()

    def __isCharLower(self, char: chr):
        return char >= 'a' and char <= 'z'

    def __isOperator(self, char: chr):
        return char == '+' or char == '-' or char == '*'
    
    def __isKeyword(self, word):
        if word == "INTEGER":
            return Token("INTEGER")
        elif word == "STRING":
            return Token("STRING")
        elif word == "IF":
                return Token("IF")
        elif word == "ELIF":
                return Token("ELIF")
        elif word == "ELSE":
                return Token("ELSE")
        elif word == "WHILE":
                return Token("WHILE")
        elif word == "WRITE":
                return Token("WRITE")
        elif word == "READ":
                return Token("READ")
        elif word == "RETURN":
                return Token("RETURN")
        else:
            return False

    def __isLogic(self,word):
        if word == "AND":
            return Token("AND")
        elif word == "OR":
            return Token("OR")
        elif word == "NOT":
            return Token("NOT")
        else:
            return False
    
    def __isBoolean(self,word):
        if word == "TRUE":
            return Token("TRUE")
        elif word == "FALSE":
            return Token("FALSE")
        else:
            return False
    
    def __isSpecialSymbol(self,word):
        if word == "(":
            return Token("(")
        elif word == ")":
            return Token(")")
        elif word == "[":
            return Token("[")
        elif word == "]":
            return Token("]")
        elif word == ":":
            return Token(":")
        else:
            return False
    
    def __isArithmetic(self,word):
        if word == "+":
            return Token("+")
        elif word == "-":
            return Token("-")
        elif word == "*":
            return Token("*")
        elif word == "/":
            return Token("/")
        elif word == "<":
            return Token("<")
        elif word == ">":
            return Token(">")
        elif word == "<=":
            return Token("<=")
        elif word == ">=":
            return Token(">=")
        elif word == "=":
            return Token("=")
        elif word == "!=":
            return Token("!=")
        else:
            return False
    
    def __isRelational(self,word):
        if word == "<":
            return Token("<")
        elif word == ">":
            return Token(">")
        elif word == "<=":
            return Token("<=")
        elif word == ">=":
            return Token(">=")
        elif word == "=":
            return Token("=")
        elif word == "!=":
            return Token("!=")
        else:
            return False
            
    def readToken(self,word,line):
        
        #state q1
        if self.__isCharLower(word[0]):
            #TODO
            return Token("id")
        
        #state q2
        if self.__isDigit(word[0]):
            #TODO
            return Token("staticNumber", word)
        
        #State q3
        if self.__isCharUpper(word[0]):
            if self.__isKeyword(word):
                return self.__isKeyword(word)
            elif self.__isLogic(word):
                return self.__isLogic(word)
            elif self.__isBoolean(word):
                return self.__isBoolean(word)
        
        #state q7
        if word == "<-":
            return Token("<-")
            
        #state q8
        if self.__isSpecialSymbol(word):
            return self.__isSpecialSymbol(word)
        
        #state q6,q7
        if self.__isArithmetic(word):
            return self.__isOperator(word)
        
        #state q9
        if word == "<-":
            return Token("<-")
        
        #state q10 ...
        if self.__isRelational(word):
            return self.__isRelational(word)
        
        else:
            raise Exception(f"Lexical analyzer [{line}]: Invalid token {word}")
        
            
                
                