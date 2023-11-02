from lexicalAnalyzer import scanner
class tyPython():
    def __init__(self, mode):
        self.mode = mode
        if mode != "interactive":
            raise Exception("Invalid mode. Use 'interactive' instead")
    
    def tyPythonFrame(self):
        
        print(" _         ____        _   _                 ")
        print("| |_ _   _|  _ \ _   _| |_| |__   ___  _ __  ")
        print("| __| | | | |_) | | | | __| '_ \ / _ \| '_ \ ")
        print("| |_| |_| |  __/| |_| | |_| | | | (_) | | | |")
        print("\__|\__,  |_|    \__, |\__|_| |_|\___/|_| |_|")
        print("     |___/       |___/ ")
        print("")
        print("tyPython 0.1 - type 'help' for more information")
        
    def showHelp(self):
        
        print("")
        print("help - display this message")
        print("")
        print("run <file> - run a tyPython file with relative path")
        print("runabs <file> - run a tyPython file with absolute path")
        print("       - OBS: Only .tpy files are accepted")
        print("")
        print("exit - exit the tyPython interpreter")
    
    def typeSyntax(self,file):
        # Verifies if the file is a tyPython file ".typ"
        file = file.split(".")
        try:
            if file[1] != "tpy":
                print("Invalid file type. Use '.tpy' instead")
                return False
            else:
                return True
        except:
            print("Invalid file type. Use '.tpy' instead")
            return False
        
    def run(self, file):
        if (self.typeSyntax(file)):
            print("Running file " + file)
            tokens = scanner(file)
            
    
    def runabs(self, file):
        self.typeSyntax(file)
        print("Running file " + file)