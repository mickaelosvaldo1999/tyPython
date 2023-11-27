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
#RETURN 19
#FUNCTION 20
#IDENTIFIER 21
#booltype 22

# Grammar
# P -> : S :
# S -> A | I | L | W | R | F | V | ε
# V -> T "id"; S
# T -> INTEGER | STRING | BOOLEAN | REAL
# A -> "id" <- D; S | "id" <- EXP; S
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

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, syntax_tree):
        self.visit_node(syntax_tree)

    def visit_node(self, node, current_scope=None):
        if node.type == "P":
            # Nó do programa, percorre os nós filhos
            for son in node.sons:
                self.visit_node(son, current_scope)

        elif node.type == "V":
            # Nó de declaração de variável
            data_type = node.sons[0].type
            identifier = node.sons[1].value

            if identifier in self.symbol_table.get(current_scope, {}):
                raise Exception(f"Semantic error: Variable '{identifier}' already declared in the current scope.")

            self.symbol_table.setdefault(current_scope, {})[identifier] = data_type

        elif node.type == "A":
            # Nó de atribuição
            identifier = node.sons[0].value
            assigned_type = self.get_expression_type(node.sons[2], current_scope)

            if identifier not in self.symbol_table.get(current_scope, {}):
                raise Exception(f"Semantic error: Variable '{identifier}' not declared in the current scope.")

            declared_type = self.symbol_table[current_scope][identifier]

            if assigned_type != declared_type:
                raise Exception(f"Semantic error: Type mismatch in assignment for variable '{identifier}'.")

        elif node.type == "F":
            # Nó de definição de função
            function_name = node.sons[1].value
            return_type = node.sons[0].type

            if function_name in self.symbol_table.get(current_scope, {}):
                raise Exception(f"Semantic error: Function '{function_name}' already declared in the current scope.")

            self.symbol_table.setdefault(current_scope, {})[function_name] = return_type

            # Percorre o corpo da função
            self.visit_node(node.sons[-1], function_name)

        elif node.type == "RETURN":
            # Nó de instrução de retorno
            return_type = self.get_expression_type(node.sons[0], current_scope)

            if current_scope is None or current_scope not in self.symbol_table:
                raise Exception("Semantic error: Return statement outside of a function.")

            expected_return_type = self.symbol_table[current_scope]
            
            if return_type != expected_return_type:
                raise Exception("Semantic error: Return type mismatch in function.")

        else:
            # Caso padrão, visita os nós filhos
            for son in node.sons:
                self.visit_node(son, current_scope)

    def get_expression_type(self, expression_node, current_scope):
        if expression_node.type == "INTEGER":
            return "INTEGER"
        elif expression_node.type == "REAL":
            return "REAL"
        elif expression_node.type == "BOOLEAN":
            return "BOOLEAN"
        elif expression_node.type == "IDENTIFIER":
            identifier = expression_node.value

            if current_scope is None or current_scope not in self.symbol_table:
                raise Exception("Semantic error: Variable used outside of a valid scope.")

            if identifier not in self.symbol_table[current_scope]:
                raise Exception(f"Semantic error: Variable '{identifier}' not declared in the current scope.")

            return self.symbol_table[current_scope][identifier]

        elif expression_node.type in ["+", "-", "*", "/"]:
            left_type = self.get_expression_type(expression_node.sons[0], current_scope)
            right_type = self.get_expression_type(expression_node.sons[1], current_scope)

            if left_type == right_type:
                return left_type
            else:
                raise Exception("Semantic error: Type mismatch in arithmetic expression.")

        elif expression_node.type in [">", "<", ">=", "<=", "=", "!="]:
            left_type = self.get_expression_type(expression_node.sons[0], current_scope)
            right_type = self.get_expression_type(expression_node.sons[1], current_scope)

            if left_type == right_type:
                return "BOOLEAN"
            else:
                raise Exception("Semantic error: Type mismatch in relational expression.")

        else:
            raise Exception(f"Semantic error: Unsupported expression type '{expression_node.type}'.")

def semantic_analyzer(syntax_tree):
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(syntax_tree)
    return semantic_analyzer.symbol_table
