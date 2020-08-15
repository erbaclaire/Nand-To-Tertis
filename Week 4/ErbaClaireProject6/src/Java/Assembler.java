import java.util.*;
import java.io.*;
    
public class Assembler {
    
    // function to convert decimal to binary
    public static String convertToBinary(int n) {
	String x = "";
	while (n>0) {
	    int r = n % 2;
	    if (r == 1) {
		n = (int) n/2;
	    }
	    else {
		n = n/2;
	    }
	    x = Integer.toString(r) + x;
	}
	int lim = 16-x.length();
	for (int i=0; i < lim; i++) {
	    x = "0" + x;
	}
	return x;
     }

    // function to remove whitespaces and comments - TO DO
    
    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {

	// destination code converter lookup
	Hashtable<String, String> dests = new Hashtable<String, String>();
	dests.put("null", "000");
	dests.put("A", "100");
	dests.put("D", "010");
	dests.put("M", "001");
	dests.put("AD", "110");
	dests.put("DA", "110");
	dests.put("AM", "101");
	dests.put("MA", "101");
	dests.put("MD", "011");
	dests.put("DM", "011");
	dests.put("AMD", "111");
	dests.put("MAD", "111");
	dests.put("DAM", "111");
	dests.put("ADM", "111");
	dests.put("MDA", "111");
	dests.put("DMA", "111");

	// computation code converter lookup
	Hashtable<String, String> comps = new Hashtable<String, String>();
	comps.put("0", "0101010");
	comps.put("1", "0111111");
	comps.put("-1", "0111010");
	comps.put("D", "0001100");
	comps.put("A", "0110000");
	comps.put("M", "1110000");
	comps.put("!D", "0001101");
	comps.put("!A", "0110001");
	comps.put("!M", "1110001");
	comps.put("-D", "0001111");
	comps.put("-A", "0110011");
	comps.put("-M", "1110011");
	comps.put("D+1", "0011111");
	comps.put("1+D", "0011111");
	comps.put("A+1", "0110111");
	comps.put("1+A", "0110111");
	comps.put("M+1", "1110111");
	comps.put("1+M", "1110111");
	comps.put("D-1", "0001110");
	comps.put("A-1", "0110010");
	comps.put("M-1", "1110010");
	comps.put("D+A", "0000010");
	comps.put("A+D", "0000010");
	comps.put("D+M", "1000010");
	comps.put("M+D", "1000010");
	comps.put("D-A", "0010011");
	comps.put("D-M", "1010011");
	comps.put("A-D", "0000111");
	comps.put("M-D", "1000111");
	comps.put("D&A", "0000000"); 
        comps.put("A&D", "0000000");
	comps.put("D&M", "1000000");
	comps.put("M&D", "1000000");
	comps.put("D|A", "0010101");
	comps.put("A|D", "0010101");
	comps.put("D|M", "1010101");
	comps.put("M|D", "1010101");

	// jump code converter lookup
	Hashtable<String, String> jumps = new Hashtable<String, String>();
	jumps.put("null", "000");
	jumps.put("JLT", "100");
	jumps.put("JEQ", "010");
	jumps.put("JGT", "001");
	jumps.put("JLE", "110");
	jumps.put("JNE", "101");
	jumps.put("JGE", "011");
	jumps.put("JMP", "000");
	
	// initial symbol table
	Hashtable<String, String> symbol_table = new Hashtable<String, String>();
	symbol_table.put("SP", "0000000000000000");
	symbol_table.put("LCL", "0000000000000001");
	symbol_table.put("ARG", "0000000000000010");
	symbol_table.put("THIS", "0000000000000011");
	symbol_table.put("THAT", "0000000000000100");
	symbol_table.put("R0", "0000000000000000");
	symbol_table.put("R1", "0000000000000001");
	symbol_table.put("R2", "0000000000000010");
	symbol_table.put("R3", "0000000000000011");
	symbol_table.put("R4", "0000000000000100"); 
        symbol_table.put("R5", "0000000000000101");
	symbol_table.put("R6", "0000000000000110");
	symbol_table.put("R7", "0000000000000111");
	symbol_table.put("R8", "0000000000001000");
	symbol_table.put("R9", "0000000000001001");
	symbol_table.put("R10", "0000000000001010");
	symbol_table.put("R11", "0000000000001011");
	symbol_table.put("R12", "0000000000001100");
	symbol_table.put("R13", "0000000000001101");
	symbol_table.put("R14", "0000000000001110");
        symbol_table.put("R15", "0000000000001111");
	symbol_table.put("SCREEN", "0100000000000000");
	symbol_table.put("KBD", "0110000000000000");

	// command line file argument
	String asm_file = new String(args[0]);
	String [] splitting = asm_file.split("\\.");
	String hack_file = new String(splitting[0] + ".hack");	

	// file to write to
	PrintWriter writer = new PrintWriter(hack_file, "UTF-8");
	
	// read in file and save lines as strings to a list
	Scanner input = new Scanner(new File(asm_file)); 
	List<String> line_list = new ArrayList<String>(); 
	while (input.hasNextLine()) {
	    line_list.add(input.nextLine());
	}

	// first pass: add L Command symbols to the symbol table
	int PC = 0;
	for (int i=0; i<line_list.size(); i++) {
	    Command command = new Command(line_list.get(i));
	    String command_type = new String(command.commandType());
	    // Increase PC for each A/C Command encountered
	    if (!command_type.equals("L_COMMAND")) {
		PC++;
	    }
	    // Add symbol from L Command to the symbol table with the corresponding PC in binary
	    if (command_type.equals("L_COMMAND")) {
		int n = PC;
		symbol_table.put(command.symbol(), convertToBinary(n));
	    }
	}
	
	// second pass: .asm --> binary translation
	int register = 16;
	for (int i=0; i<line_list.size(); i++) {
	    // for each line create a new command object and find its type
	    Command command = new Command(line_list.get(i));
	    System.out.println(command);
	    String command_type = new String(command.commandType());
	    // for C commands
	    if (command_type.equals("C_COMMAND")) {
		System.out.println(command.translateCommand(dests, comps, jumps));
		writer.println(command.translateCommand(dests, comps, jumps));
	    }
	    // for A commands
	    else if (command_type.equals("A_COMMAND") && command.aIsInt()) {
		System.out.println(convertToBinary(Integer.parseInt(command.symbol())));
		writer.println(convertToBinary(Integer.parseInt(command.symbol())));
	    }
	    else if (command_type.equals("A_COMMAND") && symbol_table.containsKey(command.symbol())) {
		System.out.println(symbol_table.get(command.symbol()));
		writer.println(symbol_table.get(command.symbol()));
	    }
	    else if (command_type.equals("A_COMMAND") && !symbol_table.containsKey(command.symbol())) {
		symbol_table.put(command.symbol(), convertToBinary(register));
		register++;
		System.out.println(symbol_table.get(command.symbol()));
		writer.println(symbol_table.get(command.symbol()));
	    }
	}
	writer.close();

    }
}
			       
	
		
		
	    
    
		  
