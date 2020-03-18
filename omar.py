from InstractionSet import OPTAB

f = open("SIC_input.asm", "r")
firstLine=f.readline()
firstLineOpcode=firstLine[9:16].strip()
operand=firstLine[16:34].strip()
LOCCTR=0
if firstLineOpcode=="START":
    STARTADDRESS=operand
    LOCCTR=int(operand,16)
#     nextLine=f.readline()
# operand=nextLine[16:34].strip()
SYMTAB={}
errors=[]
if f.mode == "r":
    for LineNumber, line in enumerate(f.readlines(), 1):
        label = line[0:8].strip()  # remove newline and spaces
        opcode = line[9:16].strip()
        operand = line[16:34].strip()
        comment = line[35:65].strip()

        if line[0] != " " and line[0] != "." :
            if label in SYMTAB:
                errors.append(f"duplicate symbol {label} Line: {LineNumber+1}") 
            else:  
              SYMTAB[label]=hex(LOCCTR)
       
        if line[0] != "." : 
            if opcode in OPTAB:
                LOCCTR+=3
            elif opcode=="WORD":
                LOCCTR+=3
            elif opcode=="RESW":
                LOCCTR+=3*int(operand)
            elif opcode=="RESB":
                LOCCTR+=int(operand)
            elif opcode=="BYTE":
                if operand[0]=='C':
                    LOCCTR+=len(operand)-3
                elif  operand[0]=='X': 
                    LOCCTR+=(len(operand)-3)//2


              
        # if line[0] != "." : 

print(SYMTAB)
print(errors)
# # for LineNumber, line in enumerate(f.readlines(), 1):
# #     label = line[0:8].strip()  # remove newline and spaces
# #     opcode = line[9:16].strip()
# #     operand = line[16:34].strip()
# #     comment = line[35:65].strip()

# #     # print(label)
# #     print(opcode)
# #     # print(operand)
# #     # print(comment)
# # # print(LOCCTR)
# def main():
#     f = open("SIC_input.asm", "r")
#     numberOfdirective = 0
#     directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW']
#     linesContainIndex = []
#     labels = []
#     opcodes = []
#     operands = []
#     comments = []
#     if f.mode == "r":
#         for LineNumber, line in enumerate(f.readlines(), 1):
#             label = line[0:8].strip()  # remove newline and spaces
#             opcode = line[9:16].strip()
#             operand = line[16:34].strip()
#             comment = line[35:65].strip()

#             if line[0] != " " and line[0] != "." :
#                 labels.append(label)
#             if line[0] != "." :    
#              opcodes.append(opcode)
#             if opcode in directives:  # check if the opcode is directive or not
#                 numberOfdirective += 1

#             if operand != "":
#                 if ',x' in operand:  # search for indexing addressing
#                     linesContainIndex.append(LineNumber)
#                 operands.append(operand)

#             if comment != "" and comment[0]=='.':
#                 comments.append(comment)

#         numberOfInstruction = len(opcodes)-numberOfdirective

#     print(f'The name of program is: {opcodes}')
#     # print(f'The number of comments is:{len(comments)}')
#     # print(f'Number of directives is: {numberOfdirective}')
#     # print(f'Number of instructions is: {numberOfInstruction}')
#     # print(f'lines contain indexed addressing: {linesContainIndex}')
    


# if __name__ == "__main__":
#     main()
