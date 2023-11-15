from lexical_analyzer import split_text, remove_coments, tokens
from syntax_analyzer import syntax_analyzer
from semantic_analyzer import semantic_analyzer
#Reading the file name
file_name = 'examples/write.tpy'

#Opening the file
file = open(file_name,'r')
#Code from file
text = file.read()
#Removing comments
text = remove_coments(text)
#Removing break lines
text = text.replace("\n"," ")
#Splitting text into lexemes
text = split_text(text)

token = []
for i in range(len(text)):
    #Creeating tokens from lexemes
    token.append(tokens(text[i]))

#Showing tokens
print(token)

#Syntax analyzer
sia =syntax_analyzer(token)
#Showing syntax tree
print('Syntax Tree')
print(sia.__repr__)

#Semantic analyzer
sea = semantic_analyzer(sia)
#Showing symbol table
print('Symbol Table')
print(sea)