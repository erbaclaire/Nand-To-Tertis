This file instructs on how to compile and run the Assembler.py code found in the src directory. 
This code translates .asm files in to .hack files and exports the results to .hack files of the same filename to the same directory where the .asm file resides.
A version of Python (any version) is assumed to be downloaded to your computer.

How to Compile the Code:
The code is written in Python, which is an interpreted language not a compiled language. This step can therefore be skipped.

How to Run the Code:
1. Open a command terminal.

2. Navigate to the src directory by typing: cd [INSERT LOCAL PATH]\ErbaClaireProject6\src
   Replace [INSERT LOCAL PATH] with the filepath that leads to the ErbaClaireProject6\ directory.
   On Linux you will have to replace \ with / due to Linux cmd line syntax.
   If your filepath has spaces you will have to enclose the filepath in quotes.

3. Run the Assembler program and translate your particular .asm file by typing in the command line: python Assembler.py [INSERT FILEPATH]
   Replace [INSERT FILEPATH] with the filepath of the .asm file relative to the src directory. For instance, if the .asm file is in the src directory then you can replace [INSERT FILEPATH] with <filename>.asm.
   If the file is in one directory up you can replace [INSERT FILEPATH] with .\<nextdirectory>\<filename>.asm (./<nextdirectory>/<filename>.asm in Linux). 
   If the file is one directory below you can replace [INSERT FILEPATH] with ..\<filename>.asm (../<filename>.asm) in Linux).
   If the file is in a completely unrelated directory you can type the full file path in the syntax of your OS.


Output:
After the above 3 steps are completed, a new <filename>.hack file will be created in the same directory as your <filename>.asm file. 
The <filename>.hack file will be the assembly language from the <filename>.asm file translated in to binary code.

Everything is in working order.