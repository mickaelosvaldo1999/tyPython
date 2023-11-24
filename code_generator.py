def insert_ident(ident):
    string = ""
    for i in range(ident):
        string = string + "    "
    return string
#converting tokens to python
def code_generator(tokens):
    #Opening the file
    file = open("code.py",'w')
    ident = 0
    types = [0,1,2,3]
    values = [16,17,18,22]
    #Writing the code
    for i in range(len(tokens)-1):
        if tokens[i] != None and i >0:
            #assign var case
            if (tokens[i][0] == 21 and not tokens[i-1][0] in types):
                if (tokens[i-1][0] == 15 and tokens[i-1][1] == ";" or tokens[i-1][1] == ":"):
                    file.write(insert_ident(ident))
                file.write(tokens[i][1])
            #"<-" case
            if (tokens[i][0] == 14):
                file.write("=")
            #values case
            elif (tokens[i][0] in values):
                file.write(tokens[i][1])
            #Break line case
            elif (tokens[i][0] == 15 and tokens[i][1] == ";"):
                if (tokens[i-2] == None):
                    file.write("\n")
                elif (tokens[i-2][0] not in types):
                    file.write("\n")
            #Special Symbols case
            elif (tokens[i][0] == 15 and tokens[i][1] != ":"):
                file.write(tokens[i][1])
            #":" case
            elif (tokens[i][0] == 15 and tokens[i-1] != None and tokens[i-1][1] == ")" ):
                file.write(tokens[i][1])
                file.write("\n")
            #WRITE case
            elif (tokens[i][0] == 8):
                file.write(insert_ident(ident))
                file.write("print")
            #READ case
            elif (tokens[i][0] == 9):
                file.write(insert_ident(ident))
                file.write(tokens[i+2][1])
                file.write(" = input()")
                tokens[i+1] = None
                tokens[i+2] = None
                tokens[i+3] = None
            #Arithmetic symbols case
            elif (tokens[i][0] == 12):
                file.write(tokens[i][1])
            #IF case
            elif (tokens[i][0] == 4):
                file.write(insert_ident(ident))
                file.write("if")
                ident = ident + 1
                aux = i+1
                while(verify_conditions(tokens[aux][0],tokens[aux][1])):
                    if (verify_equal(tokens[aux][0],tokens[aux][1])):
                        file.write("==")
                        tokens[aux] = None
                    else:
                        file.write(tokens[aux][1])
                        tokens[aux] = None
                    aux = aux+1
            #ELIF case
            elif (tokens[i][0] == 5):
                ident = ident - 1
                file.write(insert_ident(ident))
                file.write("elif")
                ident = ident + 1
                aux = i+1
                while(verify_conditions(tokens[aux][0],tokens[aux][1])):
                    if (verify_equal(tokens[aux][0],tokens[aux][1])):
                        file.write("==")
                        tokens[aux] = None
                    else:
                        file.write(tokens[aux][1])
                        tokens[aux] = None
                    aux = aux+1
            #ELSE case
            elif (tokens[i][0] == 6):
                ident = ident - 1
                file.write(insert_ident(ident))
                file.write("else:\n")
                ident = ident + 1
            #WHILE case
            elif (tokens[i][0] == 7):
                file.write(insert_ident(ident))
                file.write("while")
                ident = ident + 1
                aux = i+1
                while(verify_conditions(tokens[aux][0],tokens[aux][1])):
                    if (verify_equal(tokens[aux][0],tokens[aux][1])):
                        file.write("==")
                        tokens[aux] = None
                    else:
                        file.write(tokens[aux][1])
                        tokens[aux] = None
                    aux = aux+1
            #FUNCTION case
            elif (tokens[i][0]== 20):
                file.write("def ")
                file.write(tokens[i+1][1])
                tokens[i+1] = None
                ident = ident + 1
                aux = i+2
                while(verify_parameters(tokens[aux][0],tokens[aux][1])):
                    if(tokens[aux][1] != None):
                        file.write(tokens[aux][1])
                    tokens[aux] = None
                    aux = aux+1
            #RETURN case
            elif (tokens[i][0]== 10):
                file.write(insert_ident(ident))
                file.write("return ")
                file.write(tokens[i+1][1])
                tokens[i+1] = None
                file.write("\n")
                ident = ident - 1
    #Closing the file
    file.close()
            
def verify_conditions(token1, token2):
    if (token1 == 15 and token2== ")"):
        return False
    else:
        return True

def verify_equal(token1, token2):
    if (token1 == 13 and token2== "="):
        return True
    else:
        return False

def verify_parameters(token1, token2):
    if (token1 == 15 and token2== ")"):
        return False
    else:
        return True