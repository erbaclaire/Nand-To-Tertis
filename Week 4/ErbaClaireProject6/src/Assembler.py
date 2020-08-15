############################################################################ ASSEMBLER ##########################################################
# import python libraries
import re
import sys
import os

# initialize symbol table
symbol_addresses = {'SP':'0000000000000000', 'LCL':'0000000000000001', 'ARG':'0000000000000010', 'THIS':'0000000000000011', 'THAT':'0000000000000100',
                    'R0':'0000000000000000', 'R1':'0000000000000001', 'R2':'0000000000000010', 'R3':'0000000000000011', 'R4':'0000000000000100', 
                    'R5':'0000000000000101', 'R6':'0000000000000110', 'R7':'0000000000000111', 'R8':'0000000000001000', 'R9':'0000000000001001', 
                    'R10':'0000000000001010', 'R11':'0000000000001011', 'R12':'0000000000001100', 'R13':'0000000000001101', 'R14':'0000000000001110',
                    'R15':'0000000000001111', 'SCREEN':'0100000000000000', 'KBD':'0110000000000000'}    
# lookups to decode C-instructions - includes non-syntatically correct combinations of registers and computations (e.g., includes both MD= and DM=)
destinations = {'null':'000', 'A':'100', 'D':'010', 'M':'001', 'AD':'110', 'DA':'110', 'AM':'101', 'MA':'101', 'MD':'011', 'DM':'011', 'AMD':'111', 'MAD':'111', 'DAM':'111',
                'ADM':'111', 'MDA':'111', 'DMA':'111'}
computations = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000', 'M':'1110000', '!D':'0001101', '!A':'0110001', '!M':'1110001','-D':'0001111',
                '-A':'0110011', '-M':'1110011', 'D+1':'0011111', '1+D':'0011111', 'A+1':'0110111', '1+A':'0110111', 'M+1':'1110111', '1+M':'1110111', 'D-1':'0001110', 'A-1':'0110010', 
                'M-1':'1110010', 'D+A':'0000010', 'A+D':'0000010','D+M':'1000010', 'M+D':'1000010', 'D-A':'0010011', 'D-M':'1010011', 'A-D':'0000111', 'M-D':'1000111', 'D&A':'0000000', 
                'A&D':'0000000', 'D&M':'1000000', 'M&D':'1000000', 'D|A':'0010101', 'A|D':'0010101', 'D|M':'1010101', 'M|D':'1010101'}
                
jumps =         {'null':'000', 'JLT':'100', 'JEQ':'010', 'JGT':'001', 'JLE':'110', 'JNE':'101', 'JGE':'011', 'JMP':'111'}

# import and cleans file
def clean(filename):
    # change working directory to where <filename>.asm resides
    try:
        os.chdir(os.path.dirname(filename))
    except Exception:
        pass
    print("You are currently working in: " + os.getcwd())      
    # since you are in the directory where <filename>.asm resides you can read in the file from the command line as just filename without the path
    filename = os.path.basename(filename)
    with open(filename, 'r') as file:     # opens the .asm file
        text = file.read()    # reads in the file as a string
        text2 = re.sub(re.compile("//.*?$", re.MULTILINE),'', text)     # removes // comments
        text3 = re.sub(re.compile("/\*.*?\*/",re.DOTALL ),'', text2)    # removes anything between and including /* and */ 
        text4 = text3.replace(' ','').replace('\t','')    # removes spaces, tabs 
        text5 = "\n".join([t for t in text4.split('\n') if t!=''])    # removes empty lines                       
        return text5.split('\n')
    
# find command type - takes in one line of the .asm file
def cmdtype(command):
    if command[0] == '@':
        command_type = 'A_COMMAND'
    elif command[0] == '(':
        command_type = 'L_COMMAND'
    else:
        command_type = 'C_COMMAND'
    return command_type
    
# count ROM addresses - takes in the previous value of the rom_counter, which is initialized at -1, so that the first command will be associated with ROM address 0.
# keeps track of what value to associate with a label in first_pass method 
def rom_count(rom_counter): 
    rom_counter += 1    # rom counter increases each time an A- or C- instruction is encountered   
    return rom_counter
            
# symbol table, first pass - takes in one line of the .asm file, the current symbol table, the rom_counter from the rom_count method, and the count of the number of L commands in a row
# finds the binary value of the next ROM address past where the ROM address where (Xxx) resides and associate it with Xxx in the symbol table
def first_pass(command, symbol_addresses, rom_counter, lcommands_in_a_row):
    if lcommands_in_a_row == 0:
        first_lcommand = command[1:-1]
        rom_address = rom_counter + 1           
        symbol_addresses[command[1:-1]] = '{0:016b}'.format(rom_address)    # when a L command is encountered and the preceding command is a A- or C- instruction, Xxx gets added to the symbol table and is associated with the next ROM address 
        lcommands_in_a_row += 1
    else:
        symbol_addresses[command[1:-1]] = symbol_addresses[first_lcommand]    # when a L command is encountered but is preceded by a L command, rom address should not increase and the symbol should take the ROM address of the first L command          

# count RAM addresses - takes in one line of the .asm file where the line is an A-instruction, the current symbol table, and the previous value of the ram counter, which is initialized to 15 so the first symbol will be associated with 16.        
# keeps track of next available RAM address
def ram_count(command, symbol_addresses, ram_counter):
    # if the A-instruction is of type @digit or is already in the symbol lookup, the RAM address counter is not increased
    if command[1:].isdigit() or command[1:] in symbol_addresses:
        return ram_counter
    # if the A-instruction is of type @symbol and is not already in the symbol lookup, the RAM address counter is increased to find the next available RAM address   
    if command[1:].isdigit() == False and command[1:] not in symbol_addresses:
        ram_counter += 1
        return ram_counter  
                                                                                                                              
# translate A-instruction to binary - takes in one line of the .asm file where the line is an A-instruction, the current symbol table, and the ram_counter from the ram_count method 
def A_instruction(command, symbol_addresses, ram_counter):                              
    symbolA = command[1:]     
    # if A is @decimal, then calculate value of symbolA in binary and return it
    try:
        return '{0:016b}'.format(int(symbolA)) 
    # if A is @symbol, then find {symbolA: address}, where address is the next available RAM address (in binary) as indicated by the ram_counter
    # if symbolA is already in the symbol table, return the RAM address from the symbol table. If it does not exist in the symbol table, add {symbolA: address} to the table and return the RAM address. 
    except ValueError:                             
        if symbolA not in symbol_addresses:
            symbol_addresses[symbolA] = '{0:016b}'.format(ram_counter)
            return '{0:016b}'.format(ram_counter)                                          
        else:    
            return symbol_addresses[symbolA]
                
# translate C-instruction to binary - takes in one line of the .asm file where the line is a C-instruction and the destinations, computations, and jumps lookups from the beginning of program              
def C_instruction(command, destinations, computations, jumps):
    # 1. decode <dest> (<dest>=<comp>;<jmp> or <dest>=<comp>)
    if '=' in command:
        dest = destinations[command[:command.index('=')]]
    else:
        dest = '000'    
    # 2. decode <comp>
    # <dest>=<comp>;<jmp>
    if '=' in command and  ';' in command:
        comp = computations[command[command.index('=')+1:command.index(';')]]
    # <dest>=<comp>
    elif '=' in command and  ';' not in command:
        comp = computations[command[command.index('=')+1:]]
    # <comp>;<jmp>
    elif '=' not in command and  ';' in command:
            comp = computations[command[:command.index(';')]]
    # <comp>
    elif '=' not in command and  ';' not in command:          
        comp = computations[command]        
    # 3. decode <jump>
    if ';' in command:
        jump = jumps[command[command.index(';')+1:]]
    else:
        jump = '000' 
    return '111' + comp + dest + jump 
    
# run program
if __name__ == '__main__':
    
    # read in the .asm file from the command prompt
    try:
        clean_asm = clean(*sys.argv[1:])
    except FileNotFoundError:
        print("Sorry, your file is not in this directory") 
        
    rom_counter = -1     # initialize rom counter
    ram_counter = 15     # initialize ram counter
    lcommands_in_a_row = 0     # initialize l_commands in a row to 0
    
    #first pass - find ROM address (PC) of where @Xxx should return if (Xxx) is encountered
    for command in clean_asm:   # for each line in the .asm file
        command_type = cmdtype(command)     # find the command type
        if command_type in ['A_COMMAND', 'C_COMMAND']:  
            rom_counter = rom_count(rom_counter) # if the command is an A-instruction or a C-instruction then increase the ROM counter by 1: 
            lcommands_in_a_row = 0    
        if command_type == 'L_COMMAND':
            first_pass(command, symbol_addresses, rom_counter, lcommands_in_a_row) # if the command is a L-command then add Xxx to the symbol table and associate it with the next ROM address

    #second pass - write hack code from assembly code       
    with open(os.path.basename(str(*sys.argv[1:])).split('.')[0] + '.hack', 'w') as outFile: # outputs to a .hack file
        for command in clean_asm:   # for each line in the .asm file
            command_type = cmdtype(command) # find the command type
            if command_type == 'A_COMMAND': 
                ram_counter = ram_count(command, symbol_addresses, ram_counter) # if the command is an A-instruction of type @symbol, increase the RAM counter by 1
                outFile.write(A_instruction(command, symbol_addresses, ram_counter) + '\n')  # if the command is an A-instruction then output the return of the A_instruction method                 
            if command_type == 'C_COMMAND':
                outFile.write(C_instruction(command, destinations, computations, jumps) + '\n')     # if the command is a C-instruction then output the return of the C_instruction method   
