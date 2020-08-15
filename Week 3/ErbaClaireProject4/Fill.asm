// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// NOTES:
// Pixels go from RAM[16384] (@SCREEN) to RAM[24575] -- 256 rows with 32 16-bit registers in each row.
// The keyboard (@KBD) is at RAM[24576] -- addresses beyond this are invalid.
// Do not need to go pixel by pixel because the screen will either be all black or all white. Instead go word by word (16-bits).
// Fill screen left to right and top to bottom.
// De-fill screen right to left and bottom to top.

// Initialize Loop
@i
M=0 	

// Fill in screen with black as long as the keyboard is pressed.
(BLACK)

	// Goes to white loop if RAM[24576]=0 (i.e. keyboard not pressed).	
	@KBD
	D=M
	@WHITE
	D;JEQ 			

	// Checks if screen is at RAM[24575]. If so, we don't want to access any higher registers.
	@i
	D=M 			// D=M[i]
	@8192 			// Number of RAM addresses between Keyboard and Screen.
	D=D-A 			// D=M[i]-8192
	@BLACK
	D;JEQ 			// If M[i]-8192=0 (i.e. if you have have reached the last pixel in SCREEN) then go to (BLACK) to "wait" at that pixel until the KBD is no longer pressed.

	// Fill pixels in with black going left to right, top to bottom from last white filled pixel.
	@SCREEN
	D=A 			// Sets D=16384
	@i
	A=D+M 			// R[16384+M[i]] is selected (i.e. next pixel is selected).
	M=-1			// Sets pixel=1. R[16384+M[i]]=-1. We want it to be -1 because -1 = [1111111111111111]
	@i
	M=M+1 			// Increment M[i] by 1 for next iteration
	@BLACK
	0;JMP 			// Continue black loop

// Fill in screen with white as long as keyboard is not pressed.
(WHITE)

	// Goes to black loop if RAM[24576]=1 (i.e. keyboard is pressed).
	@KBD
	D=M
	@BLACK
	D;JGT 			

	// Checks if screen is at RAM[16384]. If so, we don't want to access any lower registers. 
	@i
	D=M 			// D=M[i]
	@WHITE
	D;JLT 			// If M[i]<0 (i.e. if you have reached the first pixel then go back to (WHITE) to "wait" at that pixel until the KBD is pressed.

	// Fill pixels in with white going backwards from last black filled pixel.
	@SCREEN
	D=A 			// Sets D=16384
	@i
	A=D+M 			// R[16384+M[i]] is selected (i.e. next pixel is selected).
	M=0				// Sets pixel=0. R[16384+M[i]]=0
	@i
	M=M-1 			// De-increments M[i] by 1 for next iteration
	@WHITE
	0;JMP 			// Continue white loop