############################################################################ VM TRANSLATOR ######################################################################
# import python libraries
import re
import sys
import os
 
# imports and removes comments and empty lines from a .vm file
# takes a file.vm ('filename') and returns a list where each element in the list is a line of the cleaned .vm text
def clean(filename):
    with open(filename, 'r') as file:     # open the .in file
        text = file.read()     # read in the file as a string
        text2 = re.sub(re.compile("//.*?$", re.MULTILINE),'', text)     # remove // comments
        text3 = re.sub(re.compile("/\*.*?\*/",re.DOTALL ),'', text2)    # remove anything between and including /* and */ 
        text4 = "\n".join([t for t in text3.split('\n') if t!=''])     # remove empty lines
        return text4.split('\n')
            
# finds the command type of each line
# takes an element ('command') from the cleaned .vm text (from the clean() method) and returns the command type
def cmdtype(command):
    if command.split()[0] in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
        command_type = 'C_ARITHMETIC'
    for i in ['push', 'pop', 'label', 'goto', 'if-goto', 'function', 'return', 'call']:
        if i in command.split()[0]:
            command_type = 'C_' + i.split('-')[0].upper()                    
    return command_type
    
# finds the first argument of the command -- note: return commands do not have a first argument and arithmetic commands take the command as the first argument
# takes an element ('command') and the command's type (from the cmdtype() method) and returns the first argument of the command 
def first_arg(command, command_type):
    if command_type == 'C_ARITHMETIC': 
        return command.split()[0]
    elif command_type != 'C_RETURN':
        return command.split()[1]

# finds the second argument of the command -- note: only push, pop, function, and call commands have a second argument
# takes an element ('command') and the command's type (fromthe cmdtype() method) and returns the second argument of the command    
def second_arg(command, command_type):
    if command_type in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
        return command.split()[2]
        
# translates push and pop commands to assembly language
# takes the command type, first argument, and second argument of the command (from the above methods) and returns the asm code associated with each push/pop command  
def pop_push(command_type, first_arg, second_arg, filename):
    
    comment = '// ' + command_type.split('_')[1].lower() + ' ' + first_arg + ' ' + second_arg + '\n'

    # before_pop de-increments the SP to get the topmost value in the stack and stores that value in the D register
    # finish_push puts the value that is in the D register into the next available stack RAM address; the SP is incremented by 1 to point to the next available stack RAM address
    before_pop = '@SP\nAM=M-1\nD=M'                                  
    finish_push = '@SP\nA=M\nM=D\n@SP\nM=M+1\n'     
    
    # pushing constants                                
    if first_arg == 'constant':
        return comment + '@' + second_arg + '\nD=A\n' + finish_push  
        
    # pushing/poping LCL, ARG, THIS, THAT                        
    lookup = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}
    if first_arg in lookup:
        segment_helper = '@' + second_arg + '\nD=A\n@' + lookup[first_arg] + '\nAD=D+M'  # note: using AD= to work for both push and pop -- will not use more tick-tock cycles
        # push - grabs the value from RAM[RAM[first_arg] + second_arg] and pushes value to the top of the stack 
        # pop - takes the topmost value in the stack and saves it to RAM[RAM[first_arg] + second_arg]   
        if command_type == 'C_PUSH':                
            return comment + segment_helper + '\nD=M\n' + finish_push
        if command_type == 'C_POP':  
            return comment + segment_helper + '\n@R13\nM=D\n' + before_pop + '\n@R13\nA=M\nM=D\n'
            
    # pushing/poping temp
    if command_type == 'C_PUSH' and first_arg == 'temp':
        return comment + '@' + str(5 + int(second_arg)) + '\nD=M\n' + finish_push
    if command_type == 'C_POP' and first_arg == 'temp':
        return comment + before_pop + '\n@' + str(5 + int(second_arg)) + '\nM=D\n'
            
    # pushing/poping static - static variables start at R[16] 
    static_start = '@' + os.path.splitext(filename)[0] + '.' + second_arg    # grabs @XXX.j where XXX is the name of the .vm file and j is the second argument of the command
    if command_type == 'C_PUSH' and first_arg == 'static':
        return comment + static_start + '\nD=M\n' + finish_push
    if command_type == 'C_POP' and first_arg == 'static':
        return comment + before_pop + '\n' + static_start + '\nM=D\n'
                     
    # pushing/poping pointer - maps bases of THIS and THAT -- note: second argument can take one of two values (0 or 1) - 0 is associated with THIS and 1 is associated with THAT
    if command_type == 'C_PUSH' and first_arg == 'pointer':
        if second_arg == '0':
            return comment + '@THIS\nD=M\n' + finish_push 
        if second_arg == '1':
            return comment + '@THAT\nD=M\n' + finish_push 
    if command_type == 'C_POP' and first_arg == 'pointer':
        if second_arg == '0':
            return comment + before_pop + '\n@THIS\nM=D\n'
        if second_arg == '1':
            return comment + before_pop + '\n@THAT\nM=D\n'
                                
# arithmetic helper to create different labels and symbols for different equalities/inequalites in the writh_arith() method, below
# takes the first argument of the command and returns an int value to concatenate to a label or symbol in the write_arith() method in order to differentiate between different equalities/inequalities  
def comparison_helper(first_arg, helper): 
    if first_arg in ['eq', 'gt', 'lt']:
        helper += 1
        return helper

# translates arithmetic commands to assembly language
# takes the first argument (ffrom the first_arg() method) and returns the asm code associated with each arithmetic command                     
def write_arith(first_arg, helper):

    comment = '// ' + first_arg + '\n' 
           
    # for one operand arithmetic - saves the output to the top of the stack; SP does not change
    if first_arg == 'neg':
        return comment + '@SP\nA=M-1\nM=-M\n'     
    if first_arg == 'not':
        return comment + '@SP\nA=M-1\nM=!M\n'
        
    # general purpose code to perform two operand operations
    grab = '@SP\nAM=M-1\nD=M\nA=A-1'  
    
    # for two operand arithmetic - takes RAM[SP-1] and RAM[SP-2] and performs the arithmetic command; saves output to RAM[SP-2]; SP gets de-incremented by 1 from its original position
    if first_arg == 'add':
        return comment + grab + '\nM=D+M\n'
    if first_arg == 'sub':
        return comment + grab + '\nM=M-D\n'                                                                 
    if first_arg == 'and':
        return comment + grab + '\nM=D&M\n'       
    if first_arg == 'or':
        return comment + grab + '\nM=D|M\n' 
    
    # comparisons - uses jumps to choose between -1 (True) and 0 (False)
    # helper creates a way to jump to different ROM positions by symbol and label relationships
    is_true_symbol = '@CONTINUE' + str(helper)
    is_true_label = '(CONTINUE' + str(helper) + ')'
    jumps = '@SP\nA=M-1\nM=0\n' + is_true_label    
    if first_arg == 'eq':
        return comment + grab + '\nD=M-D\nM=-1\n' + is_true_symbol + '\nD;JEQ\n' + jumps + '\n'
    if first_arg == 'gt':
        return comment + grab + '\nD=M-D\nM=-1\n' + is_true_symbol + '\nD;JGT\n' + jumps + '\n'
    if first_arg == 'lt':
        return comment + grab + '\nD=M-D\nM=-1\n' + is_true_symbol + '\nD;JLT\n' + jumps + '\n'
                                       
# run program
if __name__ == '__main__':
    # find .vm file(s) based on if the command line argument is a file or a directory
    if os.path.isdir(*sys.argv[1:]):
        os.chdir(*sys.argv[1:])
        files = [f for f in os.listdir() if f.endswith('.vm')]
        out = os.path.basename(str(*sys.argv[1:]) + '.asm')
    else: 
        try:
            os.chdir(os.path.dirname(*sys.argv[1:]))
        except:
            pass
        files = [os.path.basename(*sys.argv[1:])]
        out = os.path.splitext(os.path.basename(str(*sys.argv[1:])))[0] + '.asm'
        
    with open(out, 'w') as outFile:
        helper = -1
        #loop through .vm files
        for f in files:   
            print('Current file: ' + f)
            clean_vm = clean(f)
            # for each command in the cleaned .vm file generate the .asm code and output it to the 'out' file
            for command in clean_vm:    
                command_type = cmdtype(command)
                fa = first_arg(command, command_type)
                sa = second_arg(command, command_type)
                if command_type == 'C_PUSH' or command_type == 'C_POP':
                    outFile.write(pop_push(command_type, fa, sa, f) + '\n')
                if command_type == 'C_ARITHMETIC':
                    helper = comparison_helper(fa, helper)
                    outFile.write(write_arith(fa, helper) + '\n')
        outFile.write('// infinite loop\n(END)\n@END\n0;JMP\n') # infinite loop to stop program counter from moving any further down