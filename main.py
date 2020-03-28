from InstractionSet import OPTAB

import sys
SIC_File_input = str(sys.argv[1])
Intermediate_File_output = str(sys.argv[2])

inputFile = open(SIC_File_input, "r")
intermFile = open(Intermediate_File_output, "w")

firstLine = inputFile.readline()

firstLineOpcode = firstLine[9:16].strip()
operand = firstLine[16:34].strip()
nameOfProgram = firstLine[0:8].strip()

LOCCTR = 0
if firstLineOpcode == "START":
    STARTADDRESS = operand
    LOCCTR = int(operand, 16)  # make locctr integer
    # write first line to intermediate file
    intermFile.write(
        f"{format(LOCCTR,'x')}  {firstLine[0:8]} {firstLine[9:16]}{firstLine[16:34]}\n")


SYMTAB = {} 
LITTAB = {} #Literal value length address
Errors = []
if inputFile.mode == "r":
    for LineNumber, line in enumerate(inputFile.readlines(), 1):
        label = line[0:8].strip()      # remove newlines and spaces
        opcode = line[9:16].strip()
        operand = line[16:34].strip()
        # comment = line[35:65].strip()

        #  Start build symbol table SYMTAB
        if line[0] != " " and line[0] != ".": 
            if label in SYMTAB:          
                Errors.append(f"Duplicate label: {label} Line: {LineNumber+1}")
            else:
                SYMTAB[label] = format(LOCCTR, 'x')
        # End build symbol table SYMTAB

        if line[0] != ".":
            #  Start build literal table LITTAB
            if operand != '':     # if no operand the operand[0] will be out of range       
                if operand[0] == "=":
                    if operand not in LITTAB:
                        if operand[1] == 'C':
                            LenLiteral = len(operand)-4
                            LITTAB[operand] = [ operand[3:-1].encode("utf-8").hex(), LenLiteral] #add value and length

                        elif operand[1] == 'X':
                            if (len(operand)-4)%2==0:
                                LenLiteral = (len(operand)-4)//2
                                LITTAB[operand] = [ operand[3:-1], LenLiteral]
                            else:
                                Errors.append(f"Literal length must be Even: {operand} Line: {LineNumber+1}")
                        
        # End build literal table LITTAB

        # Start write to intermediate file
            intermFile.write(
                f"{format(LOCCTR,'x')}  {line[0:8]} {line[9:16]}{line[16:34]}\n")
        # End write to intermediate file

            if opcode in OPTAB:
                LOCCTR += 3
            elif opcode == "LTORG" or opcode == "END":
                for Literal in LITTAB:
                    if len(LITTAB[Literal]) == 2:  # check if the literal no addressed before
                        LITTAB[Literal].append(format(LOCCTR, 'x')) #assigned address to literals
                        LOCCTR += LITTAB[Literal][1]  # LOCCTR +length of litral
                if opcode == "END":
                    break
            elif opcode == "WORD":
                LOCCTR += 3
            elif opcode == "RESW":
                LOCCTR += 3*int(operand)
            elif opcode == "RESB":
                LOCCTR += int(operand)
            elif opcode == "BYTE":
                if operand[0] == 'C':
                    LOCCTR += len(operand)-3
                elif operand[0] == 'X':
                    LOCCTR += (len(operand)-3)//2
            else:
                Errors.append(
                    f"Invalid operation code:'{opcode}' Line:{LineNumber+1}")

intermFile.close()

programlength = format(LOCCTR-int(STARTADDRESS, 16), 'x')

print("\n\t\t\t\t \t\t\tOmar Taradeh and Ibrahim AbuSamrah")
if len(Errors) != 0:
    print("Errors: ", Errors)
else:
    print(f"SYMTAB: \n{SYMTAB} \n")
    print(f"LITTAB: \n{LITTAB} \n ")
    print("LOCCTR:", format(LOCCTR, 'x'))
    print("Program length:", programlength)
    print("PRGNAME:", nameOfProgram)
