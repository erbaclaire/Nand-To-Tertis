import java.util.*;
    
public class Command {

    private String command;
     
    public Command(String command) {
	if (command == null) throw new IllegalArgumentException("line is null");
	this.command = command;
    }

    // find command type
    public String commandType() {
	if (this.command.startsWith("@")) return new String("A_COMMAND");
	else if (this.command.startsWith("(")) return new String("L_COMMAND");
	else return "C_COMMAND";
    }

    // return symbol of A or L commands
    public String symbol() {
	if (this.commandType().equals("A_COMMAND")) return this.command.substring(1);
	else if (this.commandType().equals("L_COMMAND")) return this.command.substring(1, this.command.length()-1);
	return null;
    }

    // return type of A command
    public boolean aIsInt() {
	try {
	    Integer.parseInt(this.symbol());
	    return true;
	}
	catch (NumberFormatException e) {
	    return false;
	}
    }

    // return asm destination code of C commands
    public String dest() {
	if (this.command.indexOf('=') != -1) return this.command.substring(0, this.command.indexOf('='));
	else return new String("null"); 
    }

    // return asm computation code of C commands
    public String comp() {
	if (this.command.indexOf('=') != -1 && this.command.indexOf(';') != -1 ) return this.command.substring(this.command.indexOf('=')+1, this.command.indexOf(';'));
	else if (this.command.indexOf('=') != -1 && this.command.indexOf(';') == -1 ) return this.command.substring(this.command.indexOf('=')+1);
	else if (this.command.indexOf('=') == -1 && this.command.indexOf(';') != -1 ) return this.command.substring(0, this.command.indexOf(';'));
	else if (this.command.indexOf('=') == -1 && this.command.indexOf(';') == -1 ) return this.command;
	return null;
    }

    // return asm jump code of C commands
    public String jump() {
	if (this.command.indexOf(';') != -1) return this.command.substring(this.command.indexOf(';')+1);
	else return new String("null");
    }

    // translate dests, comps, and jumps to binary
    public String translateCommand(Hashtable<String, String> dests, Hashtable<String, String> comps, Hashtable<String, String> jumps) {
	return new String("111") + comps.get(this.comp()) + dests.get(this.dest()) + jumps.get(this.jump());
    }

    // repr
    public String toString() {
	return this.command;
    }
	    
}
	
	
		     
										     
										     
	

    
