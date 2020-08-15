### METHODOLOGY ###
# 1. read in <filename>.in as a string
# 2. remove comments using re
# 3. remove spaces, tabs, and empty lines
# 4. export cleaned text to <filename>.out

# import python libraries
import re
import sys
import os

def deCommentWhiteSpace(filename):
    
    # changes working directory to where <filename>.in resides
    try:
        os.chdir(os.path.dirname(filename))
    except Exception:
        pass
    print("You are currently working in: " + os.getcwd())
    
    # since you are in the directory where <filename>.in resides you can read in the file from the command line as just filename without the path
    filename = os.path.basename(filename)
    with open(filename, 'r') as file:                                  # opens the .in file
        text = file.read()                                              # reads in the file as a string
        text2 = re.sub(re.compile("//.*?$", re.MULTILINE),'', text)     # removes // comments
        text3 = re.sub(re.compile("/\*.*?\*/",re.DOTALL ),'', text2)    # removes anything between and including /* and */ 
        text4 = text3.replace(' ','').replace('\t','')                  # removes spaces, tabs 
        text5 = "\n".join([t for t in text4.split('\n') if t!=''])     # removes empty lines                          
 
    # exports de-commented, white-spaced text to <filename>.out 
    with open(str(filename).split('.')[0] + '.out', 'w') as outFile:
        outFile.write(text5)

if __name__ == '__main__':
    # map command line arguments to function
    try:
        deCommentWhiteSpace(*sys.argv[1:])
    except FileNotFoundError:
        print("Sorry, your file is not in this directory")
        
  
            