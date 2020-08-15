This file instructs on how to compile and run the Compiler.py code found in the src directory. 
This code translates a .jack file in to a .xml file and exports the results to the same directory where the .jack file resides.
Python3 is assumed to be downloaded to your computer.

How to Compile the Code:
The code is written in Python, which is an interpreted language not a compiled language. This step can therefore be skipped.

How to Run the Code:
1. Open a command terminal.

2. Navigate to the src directory by typing: cd [INSERT LOCAL PATH]\ErbaClaireProject10\src
   Replace [INSERT LOCAL PATH] with the filepath that leads to the ErbaClaireProject10\ directory.
   On Linux you will have to replace \ with / due to Linux cmd line syntax.
   If your filepath has spaces you will have to enclose the filepath in quotes.

3. Run the Compiler program and translate your particular .jack file (or directory of jack files) by typing in the command line: python3 Compiler.py [INSERT FILEPATH]
   Replace [INSERT FILEPATH] with the filepath of the .jack file relative to the src directory. For instance, if the .jack file is in the src directory then you can replace [INSERT FILEPATH] with <filename>.jack.
   If the file is in one directory up you can replace [INSERT FILEPATH] with .\<nextdirectory>\<filename>.jack (./<nextdirectory>/<filename>.jack in Linux). 
   If the file is one directory below you can replace [INSERT FILEPATH] with ..\<filename>.jack (../<filename>.jack) in Linux).
   If the file is in a completely unrelated directory you can type the full file path in the syntax of your OS.
   NOTE: The [INSERT FILEPATH] can be called as the exact file (e.g., ../ArrayTest/Main.jack) or the directory that houses the jack file (or files) (e.g., ../ArrayTest). The latter will translate all .jack files in
         the given directory. 


Output:
After the above 3 steps are completed, a new <filename>.xml file will be created for each jack program in the same directory as the jack file. 

Everything is in working order.