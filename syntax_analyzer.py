#INTEGER 0
#STRING 1
#REAL 2
#BOOLEAN 3
#IF 4
#ELIF 5
#ELSE 6
#WHILE 7
#WRITE 8
#READ 9
#RETURN 10
#Logical Operator 11
#Arithmetic Operator 12
#Relational Operator 13
#Assign Operator 14
#Special Symbols 15 ( ) [ ] : , ;
#Integer Numbers 16
#Real Numbers 17
#char 18
#FUNCTION 20
#IDENTIFIER 21
#booltype 22

# Grammar
# P -> : S :
# S -> A | I | L | W | R | F | V | ε
# V -> T "id"; S
# T -> INTEGER | STRING | BOOLEAN | REAL
# A -> "id" <- D; S | "id" <- EXP; S | "id" <- "FUNCTION" "(" PARAMETERS_ ")"; S
# D -> int | str | bool | real | "id"
# EXP -> D OPA D | "id" OPA "id" | D OPA "id" | "id" OPA D
# I -> "IF" "(" CONDITION ")" ":" S ":" S | "IF" "(" CONDITION ")" ":" S ":" E
# CONDITION -> id OPR C' | D OPR C'
# C' -> "id" | D | "id" OPL CONDITION | D OPL CONDITION
# OPR -> "<"|">"|"="|"!="|"<="|">="
# OPL -> "AND" | "OR" | "NOT"
# OPA -> "+" | "-" | "*" | "/" 
# E -> "ELSE" ":" S ":" S | "ELIF" "(" CONDITION ")" ":" S ":" E | "ELIF" "(" CONDITION ")" ":" S ":" S
# L -> "WHILE" "(" CONDITION ")" ":" S ":" S
# W -> "WRITE" "(" D ")" ";"
# R -> "READ" "(" "id" ")" ";"
# F -> "FUNCTION" "id" "(" PARAMETERS ")" ":" S "RETURN" D ":" S
# PARAMETERS -> T "id" | T "id" "," PARAMETERS
# PARAMETERS_ -> "id" |"id" "," PARAMETERS_

class Node:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value
        self.sons = []
    
    def add_sons(self, node):
        self.sons.append(node)

    def __repr__(self, level = 0):
        ret = "\t"*level+repr(self.type)+"\n"
        for son in self.sons:
            ret += son.__repr__(level+1)
        return ret
    
def build_tree(tokens):
    root = Node("P")
    root.add_sons(P(tokens))
    return root

def P(tokens):
    node = Node("P")
    if tokens[0][0] == 15 and tokens[0][1] == ":":
        node.add_sons(Node(15, ":"))
        tokens.pop(0)
        node.add_sons(S(tokens))
        if tokens[0][0] == 15 and tokens[0][1] == ":":
            node.add_sons(Node(15, ":"))
            tokens.pop(0)
            return node
        else:
            print(tokens[0][0], tokens[0][1])
            raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))

def S(tokens):
    node = Node("S")
    if tokens[0][0]== 21:
        node.add_sons(A(tokens))
        return node
    elif tokens[0][0] == 4:
        node.add_sons(I(tokens))
        return node
    elif tokens[0][0] == 7:
        node.add_sons(L(tokens))
        return node
    elif tokens[0][0]== 8:
        node.add_sons(W(tokens))
        return node
    elif tokens[0][0] == 9:
        node.add_sons(R(tokens))
        return node
    elif tokens[0][0] == 20:
        node.add_sons(F(tokens))
        return node
    elif tokens[0][0] == 0 or tokens[0][0] == 1 or tokens[0][0] == 2 or tokens[0][0] == 3:
        node.add_sons(V(tokens))
        return node
    else:
        return node

def V(tokens):
    node = Node("V")
    node.add_sons(T(tokens))
    if tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == ";":
            node.add_sons(Node(15, ";"))
            tokens.pop(0)
            node.add_sons(S(tokens))
            return node
        else:
            raise Exception("Syntax Error: Missing ';' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing Identifier on line " + str(tokens[0][2]))

def T(tokens):
    node = Node("T")
    if tokens[0][0]== 0:
        node.add_sons(Node(0, None))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 1:
        node.add_sons(Node(1, None))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 3:
        node.add_sons(Node(3, None))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 2:
        node.add_sons(Node(2, None))
        tokens.pop(0)
        return node
    else:
        raise Exception("Syntax Error: Missing Type on line " + str(tokens[0][2]) + " or invalid type")

def A(tokens):
    node = Node("A")
    if tokens[0][0]== 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        if tokens[0][0] == 14 and tokens[1][0] == 21 and (tokens[2][0] == 15 and tokens[2][1] =="("):
            node.add_sons(Node(14, None))
            tokens.pop(0)
            node.add_sons(Node(21, tokens[0][1]))
            tokens.pop(0)
            if tokens[0][0] == 15 and tokens[0][1] == "(":
                node.add_sons(Node(15, "("))
                tokens.pop(0)
                node.add_sons(PARAMETERS_(tokens))
                if tokens[0][0] == 15 and tokens[0][1] == ")":
                    node.add_sons(Node(15, ")"))
                    tokens.pop(0)
                    if tokens[0][0] == 15 and tokens[0][1] == ";":
                        node.add_sons(Node(15, ";"))
                        tokens.pop(0)
                        node.add_sons(S(tokens))
                        return node
                    else:
                        raise Exception("Syntax Error: Missing ';' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
        elif tokens[0][0] == 14 and tokens[2][0] != 12:
            node.add_sons(Node(14, None))
            tokens.pop(0)
            node.add_sons(D(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ";":
                node.add_sons(Node(15, ";"))
                tokens.pop(0)
                node.add_sons(S(tokens))
                return node
            else:
                raise Exception("Syntax Error: Missing ';' on line " + str(tokens[0][2]))
        elif tokens[0][0] == 14 and tokens[2][0] == 12:
            node.add_sons(Node(14, None))
            tokens.pop(0)
            node.add_sons(EXP(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ";":
                node.add_sons(Node(15, ";"))
                tokens.pop(0)
                node.add_sons(S(tokens))
                return node
            else:
                raise Exception("Syntax Error: Missing ';' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing Identifier on line " + str(tokens[0][2]) + " or invalid Identifier")

def PARAMETERS_(tokens):
    node = Node("PARAMETERS_")
    if tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == ",":
            node.add_sons(Node(15, ","))
            tokens.pop(0)
            node.add_sons(PARAMETERS_(tokens))
            return node
        else:
            return node
    else:
        raise Exception("Syntax Error: Missing Identifier on line " + str(tokens[0][2]) + " or invalid Identifier")

def D(tokens):
    node = Node("D")
    if tokens[0][0] == 18:
        node.add_sons(Node(18, tokens[0][1]))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 16:
        node.add_sons(Node(16, tokens[0][1]))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 17:
        node.add_sons(Node(17, tokens[0][1]))
        tokens.pop(0)
        return node
    elif tokens[0][0]== 22:
        node.add_sons(Node(22, tokens[0][1]))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        return node
    else:
        raise Exception("Syntax Error: Missing Data on line " + str(tokens[0][2]) + " or invalid Data")

def EXP(tokens):
    node = Node("EXP")
    if tokens[0][0] == 16:
        node.add_sons(D(tokens))
        node.add_sons(OPA(tokens))
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 17:
        node.add_sons(D(tokens))
        node.add_sons(OPA(tokens))
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 18:
        node.add_sons(D(tokens))
        node.add_sons(OPA(tokens))
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 22:
        node.add_sons(D(tokens))
        node.add_sons(OPA(tokens))
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        node.add_sons(OPA(tokens))
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        return node
    else:
        raise Exception("Syntax Error: Missing Expression on line " + str(tokens[0][2]) + " or invalid Expression")

def E(tokens):
    node = Node("E")
    if tokens[0][0] == 6:
        node.add_sons(Node(6, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == ":":
            node.add_sons(Node(15, ":"))
            tokens.pop(0)
            node.add_sons(S(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ":":
                node.add_sons(Node(15, ":"))
                tokens.pop(0)
                node.add_sons(S(tokens))
                return node
            else:
                raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
    elif tokens[0][0] == 5:
        node.add_sons(Node(5, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == "(":
            node.add_sons(Node(15, "("))
            tokens.pop(0)
            node.add_sons(CONDITION(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ")":
                node.add_sons(Node(15, ")"))
                tokens.pop(0)
                if tokens[0][0] == 15 and tokens[0][1] == ":":
                    node.add_sons(Node(15, ":"))
                    tokens.pop(0)
                    node.add_sons(S(tokens))
                    if tokens[0][0] == 15 and tokens[0][1] == ":":
                        node.add_sons(Node(15, ":"))
                        tokens.pop(0)
                        if tokens[0][0] == 5 or tokens[0][0] == 6:
                            node.add_sons(E(tokens))
                            return node
                        else:
                            node.add_sons(S(tokens))
                            return node
                    else:
                        raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))

def I(tokens):
    node = Node("I")
    if tokens[0][0] == 4:
        node.add_sons(Node(4, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == "(":
            node.add_sons(Node(15, "("))
            tokens.pop(0)
            node.add_sons(CONDITION(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ")":
                node.add_sons(Node(15, ")"))
                tokens.pop(0)
                if tokens[0][0] == 15 and tokens[0][1] == ":":
                    node.add_sons(Node(15, ":"))
                    tokens.pop(0)
                    node.add_sons(S(tokens))
                    if tokens[0][0] == 15 and tokens[0][1] == ":":
                        node.add_sons(Node(15, ":"))
                        tokens.pop(0)
                        if tokens[0][0] == 5 or tokens[0][0] == 6:
                            node.add_sons(E(tokens))
                            return node
                        node.add_sons(S(tokens))
                        return node
                    else:
                        raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
    elif tokens[0][0] == 5:
        node.add_sons(Node(5, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == "(":
            node.add_sons(Node(15, "("))
            tokens.pop(0)
            node.add_sons(CONDITION(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ")":
                node.add_sons(Node(15, ")"))
                tokens.pop(0)
                if tokens[0][0] == 15 and tokens[0][1] == ":":
                    node.add_sons(Node(15, ":"))
                    tokens.pop(0)
                    node.add_sons(S(tokens))
                    if tokens[0][0]== 15 and tokens[0][1] == ":":
                        node.add_sons(Node(15, ":"))
                        tokens.pop(0)
                        node.add_sons(S(tokens))
                        return node
                    else:
                        raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
    elif tokens[0][0] == 6:
        node.add_sons(Node(6, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == ":":
            node.add_sons(Node(15, ":"))
            tokens.pop(0)
            node.add_sons(S(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ":":
                node.add_sons(Node(15, ":"))
                tokens.pop(0)
                node.add_sons(S(tokens))
                return node
            else:
                raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing 'IF' on line " + str(tokens[0][2]) + " or invalid 'IF'")

def CONDITION(tokens):
    node = Node("CONDITION")
    if tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        node.add_sons(OPR(tokens))
        node.add_sons(C_(tokens))
        return node
    elif tokens[0][0] == 16:
        node.add_sons(D(tokens))
        node.add_sons(OPR(tokens))
        node.add_sons(C_(tokens))
        return node
    elif tokens[0][0] == 17:
        node.add_sons(D(tokens))
        node.add_sons(OPR(tokens))
        node.add_sons(C_(tokens))
        return node
    elif tokens[0][0] == 18:
        node.add_sons(D(tokens))
        node.add_sons(OPR(tokens))
        node.add_sons(C_(tokens))
        return node
    elif tokens[0][0] == 22:
        node.add_sons(D(tokens))
        node.add_sons(OPR(tokens))
        node.add_sons(C_(tokens))
        return node
    else:
        raise Exception("Syntax Error: Missing Condition on line " + str(tokens[0][2]) + " or invalid Condition")

def C_(tokens):
    node = Node("C_")
    if tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 16:
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 17:
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 18:
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 22:
        node.add_sons(D(tokens))
        return node
    elif tokens[0][0] == 11 and tokens[0][1] == "AND":
        node.add_sons(Node(11, "AND"))
        tokens.pop(0)
        node.add_sons(CONDITION(tokens))
        return node
    elif tokens[0][0] == 11 and tokens[0][1] == "OR":
        node.add_sons(Node(11, "OR"))
        tokens.pop(0)
        node.add_sons(CONDITION(tokens))
        return node
    elif tokens[0][0] == 11 and tokens[0][1] == "NOT":
        node.add_sons(Node(11, "NOT"))
        tokens.pop(0)
        node.add_sons(CONDITION(tokens))
        return node
    else:
        raise Exception("Syntax Error: Missing Condition on line " + str(tokens[0][2]) + " or invalid Condition")
    
def OPR(tokens):
    node = Node("OPR")
    if tokens[0][0] == 13 and tokens[0][1] == "<":
        node.add_sons(Node(13, "<"))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 13 and tokens[0][1] == ">":
        node.add_sons(Node(OPR, ">"))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 13 and tokens[0][1] == "=":
        node.add_sons(Node(13, "="))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 13 and tokens[0][1] == "!=":
        node.add_sons(Node(13, "!="))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 13 and tokens[0][1] == "<=":
        node.add_sons(Node(13, "<="))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 13 and tokens[0][1] == ">=":
        node.add_sons(Node(13, ">="))
        tokens.pop(0)
        return node
    else:
        raise Exception("Syntax Error: Missing Operator on line " + str(tokens[0][2]) + " or invalid Operator")

def OPA(tokens):
    node = Node("OPA")
    if tokens[0][0] == 12 and tokens[0][1] == "+":
        node.add_sons(Node(12, "+"))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 12 and tokens[0][1] == "-":
        node.add_sons(Node(12, "-"))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 12 and tokens[0][1] == "*":
        node.add_sons(Node(12, "*"))
        tokens.pop(0)
        return node
    elif tokens[0][0] == 12 and tokens[0][1] == "/":
        node.add_sons(Node(12, "/"))
        tokens.pop(0)
        return node
    else:
        raise Exception("Syntax Error: Missing Operator on line " + str(tokens[0][2]) + " or invalid Operator")

def L(tokens):
    node = Node("L")
    if tokens[0][0] == 7:
        node.add_sons(Node(7, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == "(":
            node.add_sons(Node(15, "("))
            tokens.pop(0)
            node.add_sons(CONDITION(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ")":
                node.add_sons(Node(15, ")"))
                tokens.pop(0)
                if tokens[0][0] == 15 and tokens[0][1] == ":":
                    node.add_sons(Node(15, ":"))
                    tokens.pop(0)
                    node.add_sons(S(tokens))
                    if tokens[0][0] == 15 and tokens[0][1] == ":":
                        node.add_sons(Node(15, ":"))
                        tokens.pop(0)
                        node.add_sons(S(tokens))
                        return node
                    else:
                        raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing 'WHILE' on line " + str(tokens[0][2]) + " or invalid 'WHILE'")

def W(tokens):
    node = Node("W")
    if tokens[0][0] == 8:
        node.add_sons(Node(8, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == "(":
            node.add_sons(Node(15, "("))
            tokens.pop(0)
            node.add_sons(D(tokens))
            if tokens[0][0] == 15 and tokens[0][1] == ")":
                node.add_sons(Node(15, ")"))
                tokens.pop(0)
                if tokens[0][0] == 15 and tokens[0][1] == ";":
                    node.add_sons(Node(15, ";"))
                    tokens.pop(0)
                    node.add_sons(S(tokens))
                    return node
                else:
                    raise Exception("Syntax Error: Missing ';' on line " + str(tokens[0][2]))
            else:
                print(tokens[0][0], tokens[0][1])
                raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing 'WRITE' on line " + str(tokens[0][2]) + " or invalid 'WRITE'")

def R(tokens):
    node = Node("R")
    if tokens[0][0] == 9:
        node.add_sons(Node(9, None))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == "(":
            node.add_sons(Node(15, "("))
            tokens.pop(0)
            if tokens[0][0] == 21:
                node.add_sons(Node(21, tokens[0][1]))
                tokens.pop(0)
                if tokens[0][0] == 15 and tokens[0][1] == ")":
                    node.add_sons(Node(15, ")"))
                    tokens.pop(0)
                    if tokens[0][0] == 15 and tokens[0][1] == ";":
                        node.add_sons(Node(15, ";"))
                        tokens.pop(0)
                        node.add_sons(S(tokens))
                        return node
                    else:
                        raise Exception("Syntax Error: Missing ';' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing Identifier on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
    else:
        raise Exception("Syntax Error: Missing 'READ' on line " + str(tokens[0][2]) + " or invalid 'READ'")
    return node

def F(tokens):
    node = Node("F")
    if tokens[0][0] == 20:
        node.add_sons(Node(20, None))
        tokens.pop(0)
        if tokens[0][0] == 21:
            node.add_sons(Node(21, tokens[0][1]))
            tokens.pop(0)
            if tokens[0][0] == 15 and tokens[0][1] == "(":
                node.add_sons(Node(15, "("))
                tokens.pop(0)
                node.add_sons(PARAMETERS(tokens))
                if tokens[0][0] == 15 and tokens[0][1] == ")":
                    node.add_sons(Node(15, ")"))
                    tokens.pop(0)
                    if tokens[0][0] == 15 and tokens[0][1] == ":":
                        node.add_sons(Node(15, ":"))
                        tokens.pop(0)
                        node.add_sons(S(tokens))
                        if tokens[0][0] == 10:
                            node.add_sons(Node(10, None))
                            tokens.pop(0)
                            node.add_sons(D(tokens))
                            if tokens[0][0] == 15 and tokens[0][1] == ":":
                                node.add_sons(Node(15, ":"))
                                tokens.pop(0)
                                node.add_sons(S(tokens))
                                return node
                            else:
                                print(tokens[0][0], tokens[0][1])
                                raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
                        else:
                            raise Exception("Syntax Error: Missing 'RETURN' on line " + str(tokens[0][2]) + " or invalid 'RETURN'")
                    else:
                        raise Exception("Syntax Error: Missing ':' on line " + str(tokens[0][2]))
                else:
                    raise Exception("Syntax Error: Missing ')' on line " + str(tokens[0][2]))
            else:
                raise Exception("Syntax Error: Missing '(' on line " + str(tokens[0][2]))
        else:
            raise Exception("Syntax Error: Missing Identifier on line " + str(tokens[0][2]))
    return node

def PARAMETERS(tokens):
    node = Node("PARAMETERS")
    node.add_sons(T(tokens))
    if tokens[0][0] == 21:
        node.add_sons(Node(21, tokens[0][1]))
        tokens.pop(0)
        if tokens[0][0] == 15 and tokens[0][1] == ",":
            node.add_sons(Node(15, ","))
            tokens.pop(0)
            node.add_sons(PARAMETERS(tokens))
            return node
        else:
            return node
    else:
        raise Exception("Syntax Error: Missing Identifier on line" + str(tokens[0][2]) + " or invalid Identifier")

def syntax_analyzer(tokens):
    root = build_tree(tokens)
    return root

