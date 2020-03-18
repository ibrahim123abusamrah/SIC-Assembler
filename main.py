from InstractionSet import Opcode

f = open("SIC_input.asm", "r")


for LineNumber, line in enumerate(f.readlines(), 1):
    print(line)