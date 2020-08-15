This file instructs on how to compile and run the deCommentWhiteSpace.py code found in the src directory. 
This code removes whitespace and comments from .in files and exports the results to .out files of the same filename to the same directory where the .in file resides.
A version of Python (any version) is assumed to be downloaded to your computer.

How to Compile the Code:
The code is written in Python, which is an interpreted language not a compiled language. This step can therefore be skipped.

How to Run the Code:
1. Open a command terminal.

2. Navigate to the src directory by typing: cd [INSERT LOCAL PATH]\ErbaClaireProject0\src
   Replace [INSERT LOCAL PATH] with the filepath that leads to the ErbaClaireProject0\ directory.
   On Linux you will have to replace \ with / due to Linux cmd line syntax.
   If your filepath has spaces you will have to enclose the filepath in quotes.

3. Run the removeCommentsWS program and de-comment/de-whitespace your particular file by typing in the command line: python removeCommentsWS.py [INSERT FILEPATH]
   Replace [INSERT FILEPATH] with the filepath of the .in file relative to the src directory. For instance, if the .in file is in the src directory then you can replace [INSERT FILEPATH] with <filename>.in.
   If the file is in one directory up you can replace [INSERT FILEPATH] with .\<nextdirectory>\<filename>.in (./<nextdirectory>/<filename>.in in Linux). 
   If the file is one directory below you can replace [INSERT FILEPATH] with ..\<filename>.in (../<filenmae>.in) in Linux).
   If the file is in a completely unrelated directory you can type the full file path in the syntax of your OS.


Output:
After the above 3 steps are completed, a new <filename>.out file will be created in the same directory as your <filename>.in file. 
The <filename>.out file will resemble the <filename>.in file except all comments, white spaces, and blank lines will be removed.
   