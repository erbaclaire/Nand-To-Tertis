// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectfully).

// Put your code here.
// There is no multiplication in our ALU so we need to sum R[1] R[0] times.
@i
M=1				// Sets first M[i]=1
@R2
M=0 			// Sets M[R2]=0 (this is where the multiplicative sum will be held).

(LOOP)
	@i
	D=M         // Sets D=M[i]
	@R0
	D=D-M 		// Sets D=M[i]-R[0]
	@END	
	D;JGT		// If (M[i]-R[0])>0 then go to end (i.e. if loop has run R[0] times then exit loop).
	@R1
	D=M 		// Sets D=R[1]
	@R2
	M=M+D   	// Sets R[2]=R[2]+R[1]. Increase the multiplicative sum by R[1].	
	@i
	M=M+1		// Increases M[i] by 1 for next iteration.
	@LOOP
	0;JMP		// Restart loop at next iteration.
(END)
	@END
	0;JMP 		// Unconditional jump to END for infinite loop.




