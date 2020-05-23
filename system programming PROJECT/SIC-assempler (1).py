from InstractionSet import OPTAB
import sys
def pass1(): 
        global STARTADDRESS
        global programlength
        global nameOfProgram
        
        # SIC_File_input = str(sys.argv[1])
        # Intermediate_File_output = str(sys.argv[2])
        SIC_File_input="SIC_inputLiteral.asm"
        Intermediate_File_output="Intermediatefile.txt"

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
                f"{format(LOCCTR,'x').upper()}  {firstLine[0:8]} {firstLine[9:16]}{firstLine[16:34]}\n")
         #Literal value length address
        
        if inputFile.mode == "r":
            for LineNumber, line in enumerate(inputFile.readlines(), 2):
                label = line[0:8].strip()      # remove newlines and spaces
                opcode = line[9:16].strip()
                operand = line[16:34].strip()
                # comment = line[35:65].strip()

                #  Start build symbol table SYMTAB
                if line[0] != " " and line[0] != ".": 
                    if label in SYMTAB:          
                      print(f"Errors: Duplicate label: {label} Line: {LineNumber}")
                      return 0
                    else:
                        SYMTAB[label] = format(LOCCTR, 'x').upper()
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
                                         print(f"Errors: Literal length must be Even: {operand} Line: {LineNumber}")
                                         return 0                
                # End build literal table LITTAB

                # Start write to intermediate file
                    
                    intermFile.write(
                        f"{format(LOCCTR,'x').upper()}  {line[0:8]} {line[9:16]}{line[16:34]}")
                # End write to intermediate file

                    if opcode in OPTAB:
                        LOCCTR += 3
                    elif opcode == "LTORG" or opcode == "END":
                        for Literal in LITTAB:
                            if len(LITTAB[Literal]) == 2:  # check if the literal no addressed before
                                LITTAB[Literal].append(format(LOCCTR, 'x')) #assigned address to literals
                                
                                intermFile.write(
                                        f"{format(LOCCTR,'x').upper()}    -      {Literal}\n")
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
                       print(f"Errors: Invalid operation code:'{opcode}' Line:{LineNumber}")
                       return 0

        intermFile.close()

        programlength = format(LOCCTR-int(STARTADDRESS, 16), 'x')
        print("\n\t\t\t\t \t\t\tOmar Taradeh and Ibrahim AbuSamrah")
        
        print(f"SYMTAB: \n{SYMTAB} \n")
        if len(LITTAB)!=0:
            print(f"LITTAB: \n{LITTAB} \n ")
        print("LOCCTR:", format(LOCCTR, 'x').upper())
        print("Program length:", programlength.upper())
        print("PRGNAME:", nameOfProgram)

def pass2():
    ListnFile=open("ListingFile.txt","w")
    objectFileWr=open("objectFile.txt","w")
    intermFile = open("Intermediatefile.txt", "r")
    
    firstline=intermFile.readline()
    FirLineOpcod=firstline[15:22].strip()
    if FirLineOpcod=="START":
        ListnFile.write(firstline)
    objectFileWr.write(f"H^{'{:<6}'.format(nameOfProgram)}^{'{:0>6}'.format(STARTADDRESS.upper())}^{'{:0>6}'.format(programlength.upper())}\n")#align right and padding character with 0
    
    addressList=[]
    objCodList=[]
    
    for linenumber,line in enumerate(intermFile.readlines(),2):
        loca=line[0:6].strip()    
        opcode = line[15:22].strip()
        operand = line[22:35].strip()
        if opcode=="LTORG":
            continue
       
        if opcode in OPTAB:
            if operand=="":  #if not found a symbol  (RSUB)
                operandAddress="0000"
                # print(f"Error undefined symbol: '{operand}' line:{linenumber}")
            elif operand[-2:]==",X":#check if opernad  indexed
                operand=operand[:-2]
                if operand in SYMTAB:
                    MSD=int(SYMTAB[operand][0])+8   #msd+1000
                    operandAddress=str(MSD)+SYMTAB[operand][1:]
                else:
                    operandAddress="0000"
                    print(f"Error undefined symbol: '{operand}' line:{linenumber}, so next object code not vaild")
  
            elif operand in SYMTAB:
                operandAddress=SYMTAB[operand]
            elif operand in LITTAB:
                operandAddress=LITTAB[operand][2]
            else:
                operandAddress="0000"
                print(f"Error undefined symbol: '{operand}' line:{linenumber}, so next object code not vaild")
                    
            assembleCode=OPTAB[opcode]+operandAddress
        elif opcode=="WORD":
            #if the opernad of direvrive word is -ve or +ve it handled
            assembleCode='{:{fill}6X}'.format(int(operand) & (2**24-1),fill=0)
        elif opcode=="BYTE":
            if   operand[0]=="C":
               assembleCode= operand[2:-1].encode("utf-8").hex()
            elif operand[0]=="X":
                assembleCode=operand[2:-1]
        elif opcode in LITTAB:

            assembleCode=LITTAB[opcode][0]
        else:
            assembleCode="-"
        ListnFile.write(f"{'{0:<30}{1:>30}'.format(line.strip(), assembleCode)}\n")

        if opcode=="END":
            break
        addressList.append(loca)         #add addresses to list
        objCodList.append(assembleCode.upper()) #add object codes to list
   
    countByte=0
    firstText=True
    codeLine=""
    i=0
    disconnect=False
    for index, obj in enumerate(objCodList,0):
        if obj=="-":
            disconnect=True
            i+=1
            continue

        countByteHex='{:x}'.format(countByte)
        if disconnect:
            
            objectFileWr.write(f"\nT^{'{:0>6}'.format(addressList[index-i].upper())}^{'{:0>2}'.format(countByteHex.upper())}{codeLine}")
            countByte=0
            codeLine=""
            i=0
            disconnect=False

        if countByte+len(obj)//2>30:
            
            if firstText: 
                objectFileWr.write(f"T^{'{:0>6}'.format(STARTADDRESS.upper())}^{'{:0>2}'.format(countByteHex.upper())}{codeLine}")
                firstText=False           
            else:
                objectFileWr.write(f"\nT^{'{:0>6}'.format(addressList[index-i].upper())}^{'{:0>2}'.format(countByteHex.upper())}{codeLine}")
            countByte=0
            codeLine=""
            i=0
        codeLine+='^'+obj
        countByte+=len(obj)//2
        i+=1
        # print the last line(not End) in object code
    countByteHex='{:x}'.format(countByte)
    objectFileWr.write(f"\nT^{'{:0>6}'.format(addressList[index-i+1].upper())}^{'{:0>2}'.format(countByteHex.upper())}{codeLine}")
    objectFileWr.write(f"\nE^{'{:0>6}'.format(STARTADDRESS.upper())}")

    ListnFile.close()
    objectFileWr.close()
    intermFile.close()
if __name__ == "__main__":
    # global variables
    SYMTAB = {}
    LITTAB={} 
    STARTADDRESS=""
    programlength=""
    nameOfProgram=""
    pass1()
    pass2()