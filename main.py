from tyPythonSetup import tyPython
    
def main():
    control = True
    tpy = tyPython("interactive")
    # Creating a scanner for the input file
    
    # tyPython initial setup
    tpy.tyPythonFrame()
    while (control):
        # Getting the input from the user
        chat = str(input(">>> "))
        chat = chat.split(" ")
        
        if chat[0] == "help":
            tpy.showHelp()
        elif chat[0] == "exit":
            control = False
        elif chat[0] == "run":
            tpy.run(chat[1])
        elif chat[0] == "runabs":
            tpy.runabs(chat[1])
        else:
            print("Invalid command. Type 'help' for more information")
        

if __name__ == "__main__":
    main()