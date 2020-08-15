This file instructs on how to compile and run the vmTranslator.py code found in the src directory. 
This code translates .vm files in to one single .asm file and exports the results to .asm files of the same filename to the same directory where the .vm file resides.
A version of Python (any version) is assumed to be downloaded to your computer.

How to Compile the Code:
The code is written in Python, which is an interpreted language not a compiled language. This step can therefore be skipped.

How to Run the Code:
1. Open a command terminal.

2. Navigate to the src directory by typing: cd [INSERT LOCAL PATH]\ErbaClaireProject7\src
   Replace [INSERT LOCAL PATH] with the filepath that leads to the ErbaClaireProject7\ directory.
   On Linux you will have to replace \ with / due to Linux cmd line syntax.
   If your filepath has spaces you will have to enclose the filepath in quotes.

3. Run the vmTranslator program and translate your particular .vm file by typing in the command line: python vmTranslator.py [INSERT FILEPATH]
   Replace [INSERT FILEPATH] with the filepath of the .vm file relative to the src directory. For instance, if the .vm file is in the src directory then you can replace [INSERT FILEPATH] with <filename>.vm.
   If the file is in one directory up you can replace [INSERT FILEPATH] with .\<nextdirectory>\<filename>.vm (./<nextdirectory>/<filename>.vm in Linux). 
   If the file is one directory below you can replace [INSERT FILEPATH] with ..\<filename>.vm (../<filename>.vm) in Linux).
   If the file is in a completely unrelated directory you can type the full file path in the syntax of your OS.
   NOTE: The [INSERT FILEPATH] can be called as the exact file (e.g., ../SimpleAdd/SimpleAdd.vm) or the directory that houses the vm file (e.g., ../SimpleAdd)


Output:
After the above 3 steps are completed, a new <filename>.asm file will be created in the same directory as your <filename>.vm file. 
The <filename>.asm file will be the vm language from the <filename>.vm file translated in to assembly language.

Everything is in working order.