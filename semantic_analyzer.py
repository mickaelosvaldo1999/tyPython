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
        self.symbol_tables_stack = [{}]

    def analyze(self, syntax_tree):
        self.visit_node(syntax_tree)

    def visit_node(self, node):
        if node.type == "V":
            self.handle_variable_declaration(node)
        elif node.type == "R":
            self.handle_read_statement(node)
        elif node.type == "A":
            self.handle_assignment(node)
        elif node.type == "F":
            self.handle_function_declaration(node)

        for son in node.sons:
            self.visit_node(son)

    def handle_variable_declaration(self, node):
        if node.sons[0].sons[0].type == 0:
            data_type = "INTEGER"
        elif node.sons[0].sons[0].type == 1:
            data_type = "STRING"
        elif node.sons[0].sons[0].type == 3:
            data_type = "BOOLEAN"
        elif node.sons[0].sons[0].type == 2:
            data_type = "REAL"

        variable_name = node.sons[1].value

        current_symbol_table = self.symbol_tables_stack[-1]

        current_symbol_table[variable_name] = data_type

    def handle_read_statement(self, node):
        variable_name = node.sons[2].value

        # Check local scopes first
        for symbol_table in reversed(self.symbol_tables_stack):
            if variable_name in symbol_table:
                return  # Variable found in local scope

        # Check global scope
        if variable_name not in self.symbol_tables_stack[0]:
            raise Exception(f"Semantic Error: Variable '{variable_name}' not declared before reading.")

    def handle_assignment(self, node):
        variable_name = node.sons[0].value

        # Check local scopes first
        for symbol_table in reversed(self.symbol_tables_stack):
            if variable_name in symbol_table:
                data_declare = symbol_table[variable_name]
                break
        else:
            # Variable not found in any local scope, check global scope
            if variable_name not in self.symbol_tables_stack[0]:
                raise Exception(f"Semantic Error: Variable '{variable_name}' not declared before assignment.")
            data_declare = self.symbol_tables_stack[0][variable_name]

        self.visit_node(node.sons[2])

        data_assign = data_declare

        if data_assign != data_declare:
            raise Exception(f"Semantic Error: Variable '{variable_name}' is of type '{data_declare}' and cannot be assigned to '{data_assign}'.")

    def check_variable_type(self, variable_name):
        variable_name_without_spaces = "".join(variable_name.split())
        # Check local scopes first
        for symbol_table in reversed(self.symbol_tables_stack):
            if variable_name_without_spaces in symbol_table:
                return symbol_table[variable_name_without_spaces]
            parameter_name = "PARAMETER " + variable_name_without_spaces
            if parameter_name in symbol_table:
                return symbol_table[parameter_name]
            
        # Check global scope
        if variable_name not in self.symbol_tables_stack[0]:
            raise Exception(f"Semantic Error: Variable '{variable_name}' not declared.")
        
        return self.symbol_tables_stack[0][variable_name]

    def handle_function_declaration(self, node):
        function_name = "FUNCTION " + node.sons[1].value

        # Parameters
        self.check_parameters(node.sons[3], function_name)

        # Enter a new local scope for the function, inheriting parameters
        self.symbol_tables_stack.append(self.symbol_tables_stack[-1].copy())

        # Body
        self.visit_node(node.sons[6])

        current_symbol_table = self.symbol_tables_stack.pop(0)

        if function_name in current_symbol_table:
            raise Exception(f"Semantic Error: Function '{function_name}' already declared.")

        if node.sons[8].sons[0].type == 21:
            # Check the type of the variable in the symbol table
            type_function = self.check_variable_type(node.sons[8].sons[0].value)
        elif node.sons[8].sons[0].type == 18:
            type_function = "STRING"
        elif node.sons[8].sons[0].type == 16:
            type_function = "INTEGER"
        elif node.sons[8].sons[0].type == 17:
            type_function = "REAL"
        elif node.sons[8].sons[0].type == 22:
            type_function = "BOOLEAN"

        current_symbol_table[function_name] = type_function
        self.symbol_tables_stack.insert(0, {function_name: type_function})

    def check_parameters(self, parameters_node, function_name):
        current_symbol_table = self.symbol_tables_stack[-1]

        if len(parameters_node.sons) == 0:
            return

        parameter_name_declare = 'PARAMETER ' + parameters_node.sons[1].value

        if parameter_name_declare in current_symbol_table:
            raise Exception(f"Semantic Error: Parameter '{parameter_name_declare}' already declared.")

        if parameters_node.sons[0].sons[0].type == 0:
            parameter_type_declare = "INTEGER"
        elif parameters_node.sons[0].sons[0].type == 1:
            parameter_type_declare = "STRING"
        elif parameters_node.sons[0].sons[0].type == 3:
            parameter_type_declare = "BOOLEAN"
        elif parameters_node.sons[0].sons[0].type == 2:
            parameter_type_declare = "REAL"

        current_symbol_table[parameter_name_declare] = parameter_type_declare

        if len(parameters_node.sons) > 3:
            self.check_parameters(parameters_node.sons[3], function_name)


def semantic_analyzer(syntax_tree):
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(syntax_tree)
    return semantic_analyzer.symbol_tables_stack
