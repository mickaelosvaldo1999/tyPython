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
#STRING 18
#FUNCTION 20
#IDENTIFIER 21
def remove_coments(text):
    start_index = text.find('$')

    while start_index != -1:
        end_index = text.find('$', start_index + 1)

        if end_index != -1:
            text = text[:start_index] + text[end_index + 1:]
        else:
            break

        start_index = text.find('$')
    
    return text

def finding_quo_marks(text):
    for i in range(len(text)):
        if (text[i] == '"'):
            return i
    return -1

def finding_assign(text):
    for i in range(len(text)):
        if (text[i] == '<' and text[i+1] == "-"):
            return i
    return -1


def split_text(text):
    symbols = ["(",")","[","]",":",",",";","=","<", "!",">","+","-","*","/"]
    splited_text = []
    word=""
    text += " "
    start_point = 0
    aux = 0
    i = 0
    while (i < len(text)):
        if (text[i] ==" " and i == start_point):
            start_point = start_point+1
        elif (text[i] == " "):
            splited_text.append(text[start_point:i])
            start_point = i+1
        elif(text[i:i+2] == "<-" and (i == start_point)):
            splited_text.append(text[i:i+2])
            i = i+1
            start_point = i+1
        elif((text[i] in symbols) and (i == start_point)):
            splited_text.append(text[i])
            start_point = i+1
        elif(text[i] in symbols):
            if (text[start_point:i]!=''):
                splited_text.append(text[start_point:i])
                splited_text.append(text[i])
                start_point = i+1
        elif(text[i] == '"' and (i == start_point)):
            num = finding_quo_marks(text[i+1:len(text)])
            splited_text.append(text[i:(i+num+2)])
            i = i+num +1
            start_point = i+1
            if (num == -1):
                raise('Error - Missing (") ')
        #verifying if text[i] == \n
        elif(text[i] == "\n" and (i == start_point)):
            splited_text.append(text[i])
            start_point = i+1
        i= i+1
    return splited_text
    
#Checking if the text is a number
def check_number(n):
    try:
        float_n =float(n)
        if float_n.is_integer():
            return 16
        else:
            return 17
    except ValueError:
        return 0

def tokens(text, line):
    if (text == "\n"):
        return line+1
    #Return of this functios is always "TYPE, LEXEME"
    #List of keywords
    listKW= ["INTEGER", "STRING","REAL","BOOLEAN", "IF", "ELIF", "ELSE", "WHILE", "WRITE", "READ", "RETURN"]
    for i in range(len(listKW)):
        if (text == listKW[i]):
            return i,None, line
    #List of logical operators
    listLO= ["AND","OR","NOT"]
    for i in range(len(listLO)):
        if (text == listLO[i]):
            return 11, text, line
    #List of arithmetical operators
    listAO=["+","*","/","-"]
    for i in range(len(listAO)):
        if (text == listAO[i]):
            return 12,text, line
    #List of relational operators
    listRO=[">","<","<=",">=","=","!="]
    for i in range(len(listRO)):
        if (text == listRO[i]):
            return 13,text, line
    #Assign Operator
    if (text == "<-"):
        return 14,None, line
    #List of special symbols
    listSS=["(",")","[","]",":",",",";"]
    for i in range(len(listSS)):
        if (text == listSS[i]):
            return 15,text, line
    
    c_n = check_number(text)
    if (c_n != 0):
        return c_n,text, line
    if (text[0] == '"'):
        return 18,text, line
    if (text == "RETURN"):
        return 19,None, line
    if (text == "FUNCTION"):
        return 20,None, line
    if (not text.isupper()):
        return 21,text, line
    else:
        raise Exception(f"Lexical analyzer : Invalid token {text}")