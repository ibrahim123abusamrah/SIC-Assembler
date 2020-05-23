# SIC-Assembler
PROJECT NAME : SicAssember V13.00

OBJECTIVES:
-Implementing an assembler for the SIC hypothetical machine
-Improving programming skills

PROJECT DESCRIPTION:
The project is a simulation to the assembler of the SIC hypothetical machine.
Students should implement both Pass1 and Pass2 of the SIC assembler language.

Your assembler should consider all the issues:
- Directives: START, END, BYTE, WORD, RESB, RESW, LTORG
- Comments: If a source line contains a period (.) in the first byte, the entire line is treated as a comment.
- Addressing modes: Simple, Indirect
- Instruction Set: Specified in Appendix A
- Literals: literals are supported in your source code
- Errors: Your Assembler should designate the errors
You should include test files. Assume a fixed format source code with all text written in uppercase. The output of Pass 1 is:
1. Symbol Table SYBTAB: should be displayed on the screen.
2. LOCCTR, PRGLTH, PRGNAME, ...
3. Intermediate file (.mdt): Stored on the secondary storage.
The output of Pass 2:
1. The object file (.obj)
2. The listing file (.lst)
3. List of errors if happened (duplicate labels, invalid mnemonic,
inappropriate operand...).

When your source code has a fixed format, you are committed to the following dimensions:
Columns: 1-8 Label
9-9 Blank
10-15 Operation code (or Assembler directive)
16-16 Blank
17-35 Operand
36-66 Comment

If your project does not have a GUI, then you should specify all the arguments well
to the command prompt as follow (Assuming executable version stored on the C partition):
C:\> pass1 cource_file.asm intmdte_file.mdt
C:\> pass2 intmdte_file.mdt output_file.obj
Your assembler can stop execution if there are errors in Pass 1, and should indicate
its termination with appropriate messages.
