############################################################################ COMPILER ##########################################################
# import python libraries
import re
import sys
import os
 
keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
      
# import and clean file - takes the name of a jack file and returns text that removes comments and blank lines
# note: white space is not removed for use in the Tokenizer class -- if there are two identifiers next to eachother and the white space between them is already removed, it is impossible to determine where one identifier starts and the other ends
def clean(filename):
    with open(filename, 'r') as f:     # open the .jack file
        text = f.read()     # read in the file as a string
        text2 = re.sub(re.compile("//.*?$", re.MULTILINE),'', text)     # remove // comments
        text3 = re.sub(re.compile("/\*.*?\*/",re.DOTALL ),'', text2)    # remove anything between and including /* and */ 
        text4 = "\n".join([t for t in text3.split('\n') if t!=''])     # remove empty lines
        return text4.split('\n')

# tokenizer class: finds and classifies all tokens in a given .jack file
class Tokenizer:
    
    # initialize 
    # takes a cleaned jack file from the clean() method and returns initialized class variables
    def __init__(self, jack):
        self.jack = iter(jack)
        self.line = self.jack.__next__()     # grabs the first line of jack code
        self.units = self.line.split()     # splits the first line of jack code in to smaller collections of tokens based on whitespace     
        self.tokens = []    # tokens will be appended to here
        self.string_skip_counter = 0 # used for skipping units when dealing with strings
    
    # grab the next line in the cleaned .jack text
    # takes an instance of itself and grabs next line of code and then splits that line of code in to smaller collections of tokens -- tokenize is called to break out the units in self.units   
    def line_advance(self):
        try:
            self.line = self.jack.__next__()
            self.units = self.line.split()
            self.tokenize(keywords, symbols)
        except StopIteration:
            pass
    
    # aggregates portions of strings
    # takes and instance of itself and returns the rest of the string that resided in different units           
    def string_end_helper(self):
        temp_string = ''
        for t in self.units:
            if '"' not in t:
                temp_string += ' ' + t
                self.units = self.units[1:]
                self.string_skip_counter += 1
            else:
                break
        return temp_string
        
    # calls ident(), keys(), symbs(), intConst(), and strConst - which themselves break out tokens and append them to the tokens list
    # takes an instance of itself, the jack keyword and symbol lookup
    # keywords and symbols are lists of all the tokens that are keywords or symbols as defined by the jack grammar       
    def tokenize(self, keywords, symbols):
        # for each unit is a line
        for unit in self.units:
            if self.string_skip_counter == 0:   # if the string_skip_counter is 0 that means no strings have yet been found and there is no need to skip over units that were already dissected 
                self.unit = unit
                # for each unit, if the unit still has more tokens in it then continue to break out tokens
                while len(self.unit) > 0:
                    self.ident(keywords)    # call ident() first to make sure the program is not mischaracterizing keywords as identifiers or vice versa
                    self.keys(keywords)
                    self.symbs(symbols)
                    self.intConst()
                    self.strConst()
                self.units = self.units[1:]
            else:   # if the string_skip_counter is not 0 it means that the program needs to skip over tokens that were already dissected in the string_end_helper() method
                self.string_skip_counter -= 1
                pass
        # when all tokens have been extracted from a line, grab the next line by calling the unit.advance() method
        self.line_advance()
    
    # break out keyword tokens
    # takes the current unit and identifies if it begins with any keywords -- if it does extract that keyword and append it to the tokens list -- return the remaining portion of the unit          
    def keys(self, keywords):
        for element in keywords:
            if self.unit.startswith(element):
                self.tokens.append((element, 'keyword'))
                self.unit = self.unit[self.unit.find(element)+len(element):]
        return self.unit
      
    # break out symbols
    # takes the current unit and identifies if it begins with any symbols -- if it does extract that symbol and append it to the tokens list -- return the remaining portion of the unit
    def symbs(self, symbols):
        for element in symbols:
            if self.unit.startswith(element):
                self.tokens.append((element, 'symbol'))
                self.unit = self.unit[self.unit.find(element)+len(element):]
        return self.unit
            
    # break out integers
    # takes the current unit and identifies if it begins with any integer constants -- if it does extract that integer constant and append it to the tokens list -- return the remaining portion of the unit
    def intConst(self):
        try:
            if self.unit[0].isdigit():
                # find the end of the integer knowing that the max length of the integer can be 5          
                int_end = 0
                for i in range(1,min(len(self.unit),5)):    # note: use min of length of unit and 5 so there is no error if the length of the unit is < 5
                    if self.unit[i].isdigit(): 
                        int_end += 1
                    else:
                        break
                self.tokens.append((self.unit[:int_end+1], 'integerConstant'))
                self.unit = self.unit[int_end+1:]
            return self.unit
        except IndexError:
            return self.unit
          
    # break out strings
    # takes the current unit and identifies if it begins with any strings -- if it does extract that string and append it to the tokens list -- return the remaining portion of the unit
    def strConst(self):
        if self.unit.startswith('"'):
            self.string_skip_counter = 0
            # strings that had no whitespace
            if self.unit[1:].find('"') != -1:
                string_end = self.unit[1:].find('"')
                self.tokens.append((self.unit[:string_end+1], 'stringConstant'))
                self.unit = self.unit[string_end+1:]
            # strings that had whitespace -- new lines are not an issue because '\n' goes against grammar rules 
            else:
                # find the end of the string by appending the next units to the start of the string until the next " (end of string) is found
                temp_string = self.unit[1:]    
                self.units = self.units[1:]
                temp_string += self.string_end_helper()
                self.unit = self.units[0]
                temp_string += ' ' + self.unit[:self.unit.find('"')]    
                self.tokens.append((temp_string, 'stringConstant'))
                self.unit = self.unit[self.unit.find('"')+1:]
                if len(self.unit) > 0:
                    self.string_skip_counter += 1   
        return self.unit  
               
    # break out identifiers
    # takes the current unit and identifies if it begins with any identifiers -- if it does extract that identifier and append it to the tokens list -- return the remaining portion of the unit
    def ident(self, keywords):
        try:
            if (self.unit[0].isalpha() or self.unit[0] == '_'):  # note: need to check if unit is not in keywords to avoid mixing up identifiers with keywords
                if len(re.findall(r'\W', self.unit)) > 0:
                    word = self.unit[:self.unit.find(re.findall(r'\W', self.unit)[0])]
                    if word in keywords:
                        self.unit = self.unit
                    else:
                        self.tokens.append((self.unit[:self.unit.find(re.findall(r'\W', self.unit)[0])], 'identifier'))
                        self.unit = self.unit[self.unit.find(re.findall(r'\W', self.unit)[0]):]
                else:
                    if self.unit in keywords:
                        self.unit = self.unit
                    else:
                        self.tokens.append((self.unit, 'identifier'))
                        self.unit = ''
            return self.unit
        except IndexError:
            return self.unit   
            
# parser class: create hierarchy of tokens based on jack structure, statements, and expressions and output xml code
# note: the assumption is that the .jack file has correct syntax
# note: type refers to an 'int,' 'char,' or 'boolean' keyword or a className identifier    
class Parse:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.xml_code = ''
        # initialize first token
        self.token = self.tokens.__next__() 
    
    # grabs next token    
    def advance(self):
        try:
            self.token = self.tokens.__next__()   
        except StopIteration:
            pass
            
    # formats current token and returns it in xml format and then grabs next token   
    def terminal_token(self):
        # preserves the original token while also advancing to the next token
        t = self.token 
        self.advance()
        #print(self.token)
        
        return '<' + t[1] + '> ' + t[0] + ' </' + t[1] + '>\n' 
  
    ############################################################################## PROGRAM STRUCTURE #############################################################################################                
    
    # compiles all vm code associated with a jack class
    def compileClass(self):
        if self.token[0] == 'class':   
            #                               'class' keyword       className identifier         '{' symbol               classVarDec*               subroutineDec*                 '}' symbol
            self.xml_code = '<class>\n' + self.terminal_token() + self.terminal_token() + self.terminal_token() + self.compileClassVarDec() + self.compileSubroutineDec() + self.terminal_token() + '</class>\n'
            return self.xml_code
           
    # allows multiple (, type varName)* or (, varName) for classVarDec, parameterList, varDec       
    def varDecHelper(self):
        if self.token[0] == ',':
            #          ',' symbol
            xml = self.terminal_token()
            # distinguish between (, type varName)* and (, varName)* 
            if self.token[0] in ['int', 'char', 'boolean'] or self.token[1] == 'identifier':
                #   type or varName identifier  
                xml += self.terminal_token()                     
                # if the next token is an identifier then it is a (, type varName)*
                if self.token[1] == 'identifier':
                    #        varName identifier     (, type verName)* 
                    xml += self.terminal_token() + self.varDecHelper() 
                # else, then it is a (, varName)*
                else:
                    #       (, varName)*
                    xml += self.varDecHelper()
            return xml 
        else:

            return ''
    
    # returns xml code of class variable declarations                   
    def compileClassVarDec(self):
        if self.token[0] in ['static', 'field']:
            #                          'static' or 'field' keyword              type               varName identifier       (, varName)*           ';' symbol                                     classVarDec*
            return '<classVarDec>\n' +   self.terminal_token()     +    self.terminal_token() +  self.terminal_token() + self.varDecHelper() + self.terminal_token() + '</classVarDec>\n' + self.compileClassVarDec() 
        else:
            return ''   
     
    # returns xml code of subroutine declarations           
    def compileSubroutineDec(self):
        if self.token[0] in ['constructor', 'function', 'method']:
            #                            'constructor', 'function', or 'method ' keyword   'void' keyword or type     subroutineName identifier       '(' symbol               parameterList?              ')' symbol               subroutineBody                                         subroutineDec*
            return '<subroutineDec>\n' +                self.terminal_token()            +  self.terminal_token() +    self.terminal_token()   + self.terminal_token() + self.compileParameterList() + self.terminal_token() + self.compileSubroutineBody() + '</subroutineDec>\n' + self.compileSubroutineDec()  
        else:
            return ''
    
    # returns xml code of parameter lists
    def compileParameterList(self):
        if self.token[0] in ['int', 'char', 'boolean'] or self.token[1] == 'identifier': 
            #                                  type                varName identifier      (, type varName)*
            return '<parameterList>\n' + self.terminal_token() + self.terminal_token() + self.varDecHelper() + '</parameterList>\n'
        else:
            return '<parameterList>\n</parameterList>\n'

    # returns xml code of subroutine bodies
    def compileSubroutineBody(self):
        if self.token[0] == '{':
            #                                 '{' symbol                varDec*                statements                '}' symbol
            return '<subroutineBody>\n' + self.terminal_token() + self.compileVarDec() + self.compileStatements() + self.terminal_token() + '</subroutineBody>\n'
        else:
            return ''
    
    # returns xml code of subroutine variable declarations        
    def compileVarDec(self):
        if self.token[0] == 'var':
            #                          'var' keyword               type             varName identifier        (, varName)*            ';' symbol                             varDec*
            return '<varDec>\n' + self.terminal_token() + self.terminal_token() + self.terminal_token() + self.varDecHelper() + self.terminal_token() + '</varDec>\n' + self.compileVarDec() 
        else:
            return ''
            
    ############################################################################## STATEMENTS ############################################################################################# 
    
    # returns xml code of statements
    def compileStatements(self):
        statements = '<statements>\n'
        while self.token[0] in ['let', 'if', 'while', 'do', 'return']: 
            statements += self.compileLetStatement()
            statements += self.compileIfStatement()
            statements += self.compileWhileStatement()
            statements += self.compileDoStatement()
            statements += self.compileReturnStatement()
        return statements + '</statements>\n'
    
    # returns xml code for arrays called in let statements    
    def letHelper(self):
        if self.token[0] == '[':
            #            '[' symbol               expression              ']' symbol
            return self.terminal_token() + self.compileExpression() + self.terminal_token()
        else:
            return ''
    
    # returns xml code of let statements        
    def compileLetStatement(self):
        if self.token[0] == 'let':
            #                              ' let' keyword        varName identifier       '[' expression ']'?         '=' symbol                  expression              ';' symbol
            return '<letStatement>\n' + self.terminal_token() + self.terminal_token() +    self.letHelper()    + self.terminal_token() + self.compileExpression() + self.terminal_token() + '</letStatement>\n'
        else:
            return ''
    
    # returns xml code of else statements               
    def elseHelper(self):
        if self.token[0] == 'else':
            #         'else' keyword            '{' symbol               statements              '}' symbol
            return self.terminal_token() + self.terminal_token() + self.compileStatements() + self.terminal_token()
        else:
            return ''
    
    # returns xml code of if statements        
    def compileIfStatement(self):
        if self.token[0] == 'if':
            #                               'if' keyword           '(' symbol                 expression                ')' symbol            '{' symbol                statements               '}' symbol        'else' '{' statments '}'?
            return '<ifStatement>\n' + self.terminal_token() + self.terminal_token() + self.compileExpression() + self.terminal_token() + self.terminal_token() + self.compileStatements() + self.terminal_token() + self.elseHelper() + '</ifStatement>\n'
        else:
            return ''
    
    # returns xml code of while statements        
    def compileWhileStatement(self):
        if self.token[0] == 'while':
            #                               'while' keyword           '(' symbol                 expression                ')' symbol            '{' symbol                statements               '}' symbol               
            return '<whileStatement>\n' + self.terminal_token() + self.terminal_token() + self.compileExpression() + self.terminal_token() + self.terminal_token() + self.compileStatements() + self.terminal_token() + '</whileStatement>\n'
        else:
            return ''
    
    # returns xml code of do statements        
    def compileDoStatement(self):
        if self.token[0] == 'do':
            #                             'do' keyword                subroutineCall                ';' symbol
            return '<doStatement>\n' + self.terminal_token() + self.compileSubroutineCall() + self.terminal_token() + '</doStatement>\n'
        else:
            return ''
            
    # returns xml code of return statements        
    def compileReturnStatement(self):
        if self.token[0] == 'return':
            #                               'return' keyword            expression?                 ';' symbol
            return '<returnStatement>\n' + self.terminal_token() + self.compileExpression() + self.terminal_token() + '</returnStatement>\n'
        else:
            return ''
            
    ############################################################################## EXPRESSIONS ############################################################################################# 
    
    # returns xml code of (op term)* -- expressions with multiple operands
    def expressionHelper(self):
        if self.token[0] in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            #            op                    term                 (op term)*
            return self.terminal_token() + self.compileTerm() + self.expressionHelper()
        else:
            return ''
    
    # returns xml code for expressions        
    def compileExpression(self):
        term = self.compileTerm()
        if term != '':
            #                          term         (op term)*
            return '<expression>\n' + term + self.expressionHelper() + '</expression>\n'
        else:
            return ''
      
    # returns xml code for terms              
    def compileTerm(self):
        # returns xml code for terms that are integers, strings, or keyword constants
        if self.token[1] in ['integerConstant', 'stringConstant'] or self.token[0] in ['true', 'false', 'null', 'this']:
            return '<term>\n' + self.terminal_token() +'</term>\n'
        # returns xml code for terms of type: unaryOp term    
        elif self.token[0] in ['-', '~']:
            return '<term>\n' + self.terminal_token() + self.compileTerm() + '</term>\n'
        # returns xml code for terms of type: '(' expression ')'     
        elif self.token[0] == '(':
            #                       '(' symbol               expression                 ')' symbol
            return '<term>\n' + self.terminal_token() + self.compileExpression() + self.terminal_token() + '</term>\n'
        # deals with terms that start with an identifier - xml gets the identifier and grabs the next token, which is token[0] below
        if self.token[1] == 'identifier':
            xml = self.terminal_token()
            # returns xml code for terms of type: varName '[' expression ']'
            if self.token[0] == '[':
                #                   varName identifier         '[' symbol               expression               ']' symbol
                return '<term>\n' +       xml          + self.terminal_token() + self.compileExpression() + self.terminal_token() + '</term>\n'
            # returns xml code for terms of type: subroutineCall
            elif self.token[0] == '.':
                #                   varName identifier      '.' symbol         subroutineName identifier    '(' symbol                 expressionList               ')' symbol
                return '<term>\n' +        xml      + self.terminal_token() +   self.terminal_token()  + self.terminal_token() + self.compileExpressionList() + self.terminal_token() + '</term>\n'
            elif self.token[0] == '(':
                #                   subroutineName identifier     '(' symbol                    expressionList             ')' symbol                                           
                return '<term>\n' +             xml          + self.terminal_token() + self.compileExpressionList() + self.terminal_token() + '</term>\n'
            # returns xml code for terms of type: varName
            else:
                return '<term>\n' + xml + '</term>\n'
        # no more terms
        else:
            return ''
    
    # returns xml code for subroutine calls     
    def compileSubroutineCall(self):  
        #     subroutineName, className, or varName identifer  
        xml = self.terminal_token()
        if self.token[0] == '(':
            #                 '(' symbol                expressionList            ')' symbol
            return xml + self.terminal_token() + self.compileExpressionList() + self.terminal_token()
        else:
            #                 '.' symbol        subroutineName identifier    '(' symbol                  expressionList             ')' symbol
            return xml + self.terminal_token() + self.terminal_token() + self.terminal_token() + self.compileExpressionList() + self.terminal_token()
    
    # returns xml code for (, expression)*
    def eListHelper(self):
        if self.token[0] == ',':
            #           ',' symbol              expression               (, expression)*
            return self.terminal_token() + self.compileExpression() + self.eListHelper()
        else:
            return ''  
    
    # returns xml code for expression lists
    def compileExpressionList(self):
        expression = self.compileExpression()
        if expression != '':
            return '<expressionList>\n' + expression + self.eListHelper() + '</expressionList>\n'
        else:
            return '<expressionList>\n</expressionList>\n'
                                             
   
# run program
if __name__ == '__main__':
    # code for if command line argument is a file or a directory
    if os.path.isdir(*sys.argv[1:]):
        os.chdir(*sys.argv[1:])
        files = [f for f in os.listdir() if f.endswith('.jack')]
    else: 
        try:
            os.chdir(os.path.dirname(*sys.argv[1:]))
        except:
            pass
        files = [os.path.basename(*sys.argv[1:])]

    token_xml_fix = {'<':'&lt;', '>':'&gt;', '&':'&amp;'}
    #loop through jack files
    for f in files:
        '''
        # tokenizer
        with open(str(f).split('.')[0] + 'T.xml', 'w') as outFile:     # create a new .xml file for each .jack file  
            print('Current file: ' + f)
            clean_jack = clean(f)   # call the clean method on the .jack file
            # tokenize the cleaned .jack file
            t = Tokenizer(clean_jack)
            t.tokenize(keywords, symbols)
            outFile.write('<tokens>\n')
            for token in t.tokens:
                if token[0] in token_xml_fix:
                    token = (token_xml_fix[token[0]], token[1])
                outFile.write('<' + token[1] + '> ' + token[0] + ' </' + token[1] + '>\n')
            outFile.write('</tokens>\n')
        '''    
        # parser        
        with open(str(f).split('.')[0] + '.xml', 'w') as outFile:     # create a new .xml file for each .jack file  
            print('Current file: ' + f)
            clean_jack = clean(f)   # call the clean method on the .jack file
            # tokenize the cleaned .jack file
            t = Tokenizer(clean_jack)
            t.tokenize(keywords, symbols) 
            # parse the tokens that were tokenized above
            parse_object = Parse(iter(t.tokens))
            parse_object.compileClass()
            xml = parse_object.xml_code
            xml = xml.replace('<symbol> < </symbol>', '<symbol> &lt; </symbol>').replace('<symbol> > </symbol>', '<symbol> &gt; </symbol>').replace('<symbol> & </symbol>', '<symbol> &amp; </symbol>')
            # indent xml code and export
            indent_count = 0
            for line in xml.split('\n'):
                if line in ['</class>', '</classVarDec>', '</subroutineDec>', '</parameterList>', '</subroutineBody>', '</varDec>', 
                             '</statements>', '</letStatement>', '</ifStatement>', '</whileStatement>', '</doStatement>', '</returnStatement>',
                             '</expression>', '</expressionList>', '</term>']:
                    indent_count -= 1
                indented_line = indent_count*'  ' + line
                if indented_line.strip() in ['<class>', '<classVarDec>', '<subroutineDec>', '<parameterList>', '<subroutineBody>', '<varDec>', 
                                              '<statements>', '<letStatement>', '<ifStatement>', '<whileStatement>', '<doStatement>', '<returnStatement>',
                                              '<expression>', '<expressionList>', '<term>']:
                    indent_count += 1
                if indented_line != '':
                    outFile.write(indented_line + '\n')                

