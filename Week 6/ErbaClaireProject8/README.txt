This file instructs on how to compile and run the vmTranslator.py code found in the src directory. 
This code translates .vm files in to one single <directory name>.asm file and exports the results to the same directory where the .vm file resides.
A version of Python (any version) is assumed to be downloaded to your computer.

How to Compile the Code:
The code is written in Python, which is an interpreted language not a compiled language. This step can therefore be skipped.

How to Run the Code:
1. Open a command terminal.

2. Navigate to the src directory by typing: cd [INSERT LOCAL PATH]\ErbaClaireProject8\src
   Replace [INSERT LOCAL PATH] with the filepath that leads to the ErbaClaireProject8\ directory.
   On Linux you will have to replace \ with / due to Linux cmd line syntax.
   If your filepath has spaces you will have to enclose the filepath in quotes.

3. Run the vmTranslator program and translate your particular .vm file by typing in the command line: python vmTranslator.py [INSERT FILEPATH]
   Replace [INSERT FILEPATH] with the filepath of the .vm file relative to the src directory. For instance, if the .vm file is in the src directory then you can replace [INSERT FILEPATH] with <filename>.vm.
   If the file is in one directory up you can replace [INSERT FILEPATH] with .\<nextdirectory>\<filename>.vm (./<nextdirectory>/<filename>.vm in Linux). 
   If the file is one directory below you can replace [INSERT FILEPATH] with ..\<filename>.vm (../<filename>.vm) in Linux).
   If the file is in a completely unrelated directory you can type the full file path in the syntax of your OS.
   NOTE: The [INSERT FILEPATH] can be called as the exact file (e.g., ../BasicLoop/BasicLoop.vm) or the directory that houses the vm file (e.g., ../BasicLoop) -- the output file will always be named after the directory name in which it resides


Output:
After the above 3 steps are completed, a new <filename>.asm file will be created in the same directory as your <filename>.vm file. 
The <filename>.asm file will be the vm language from the <filename>.vm files translated in to assembly language.

Note: Bootstrap asm code is always output. This means that the .asm code for BasicLoop, FibonacciSeries, and SimpleFunction will no longer work. 
      To see implementations of these tests one could go to line 245 and un-comment that line and then indent line 246 and rerun vmTranslator.py.

Note: At the end of each .asm file I add an infinite loop to keep the program counter in place in case the vm file does not already have an infinite loop. Some of the test files already have an infinite loop so this text is extraneous.
      I label this loop with foldername_END_INFINITE_LOOP to ensure the label is not the same as another loop in the .asm file.

Everything is in working order.