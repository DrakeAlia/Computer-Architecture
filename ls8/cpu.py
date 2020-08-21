"""CPU functionality."""

import sys
# Daily Project (Day 1 to Day 4)
HTL = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

# Sprint 
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
    # Day 1
    # Step 1: Add the constructor to cpu.py
    # Create a 256 byts of memory and 8 general-purpose registers
    # Add PC program counter
        self.branch_table = {}
         # Create 256 bites memory
        self.ram = [0] * 256
        # 8 bit register
        self.reg = [0] * 8
        # Stack Pointer (SP)
        # self.reg[7] = 0xF4
        self.reg[7] = 255
        # Program Counter, address of the currently executing instruction   
        self.pc = 0        

        # Flags
        self.E = None
        self.L = None
        self.G = None

        # Instructions
        self.branch_table[HTL] = self.hlt_inst # Halt the CPU (and exit the emulator). 
        self.branch_table[LDI] = self.ldi_inst # Set the value of a register to an integer.
        self.branch_table[PRN] = self.prn_inst # Print numeric value stored in the given register.
        self.branch_table[MUL] = self.mul_inst # Multiply the values in two registers together and store the result in registerA.
        self.branch_table[ADD] = self.add_inst # Add the value in two registers and store the result in registerA.
        self.branch_table[PUSH] = self.push_inst # Push the value in the given register on the stack.
        self.branch_table[POP] = self.pop_inst # Pop the value at the top of the stack into the given register.
        self.branch_table[CALL] = self.call_inst # Calls a subroutine (function) at the address stored in the register.
        self.branch_table[RET] = self.ret_inst # Return from subroutine.
        # self.branch_table[NOP] = self.NOP_inst # No operation. Do nothing for this instruction.

        # Instructions for sprint challenge
        self.branch_table[CMP] = self.cmp_inst # Compare the values in two registers.
        self.branch_table[JMP] = self.jmp_inst # Jump to the address stored in the given register.
        self.branch_table[JEQ] = self.jeq_inst # If `equal` flag is set (true), jump to the address stored in the given register.
        self.branch_table[JNE] = self.jne_inst # If `E` flag is clear (false, 0), jump to the address stored in the given register.

        # Definitions
        # IR - Instruction Register, contains a copy of the currently executing instruction
        # MAR - Memory Address Register, holds the memory address we're reading or writing
        # MDR - Memory Data Register, holds the value to write or the value just read
        # R5 - Reserved as the interrupt mask (IM)
        # R6 - Reserved as the interrupt status (IS)
        # R7 - Reserved as the stack pointer (SP)

    # Step 2: Add ram methods

    # Ram read should accept the address to read and
    # Return the value stored there
    def ram_read(self, MAR):
        if MAR < len(self.ram):
            return self.ram[MAR]

    # Ram write should accept a value to write and 
    # the address to write it to
    def ram_write(self, MAR, MDR):
        if MAR < len(self.ram):
            self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        # Step 3: Implement the core of CPU's run() method
        # Step 9: Beautify your run() loop

        while True:
            # Instructions register(IR)
            IR = self.ram_read(self.pc)
            # print(IR,"\n")
            if IR in self.branch_table:
                self.branch_table[IR]()
            else:
                print("ERROR:", IR)

    # Step 4: Implement the HLT instruction handler
    def hlt_inst(self):
        exit(1)

    # Step 8: Implement a Multiply and Print the Result
    def mul_inst(self):
        # Register 1
        reg_a = self.ram_read(self.pc + 1)
        # Register 2
        reg_b = self.ram_read(self.pc + 2)

        result = self.reg[reg_a] * self.reg[reg_b]
        self.reg[reg_a] = result
        self.pc += 3

    def add_inst(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        result = self.reg[reg_a] + self.reg[reg_b]
        self.reg[reg_a] = result
        self.pc += 3

    # Step 5: Add the LDI instruction
    def ldi_inst(self):
        MAR = self.ram_read(self.pc + 1)
        MDR = self.ram_read(self.pc + 2)

        if MAR < len(self.ram):
            self.reg[MAR] = MDR
        # Increment program counter by 3 steps inside the RAM
        self.pc += 3

    # Step 6: Add the PRN instruction
    def prn_inst(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    # Step 10: Implement System Stack
    def push_inst(self):
        # Decrement the stack pointer
        self.reg[7] -= 1
        operand_a = self.ram_read(self.pc + 1)
        # Store value from reg to ram
        self.ram[self.reg[7]] = self.reg[operand_a]
        self.pc += 2

    # Step 10: Implement System Stack
    def pop_inst(self):
        # Read value of SP and overwrite next register
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.ram_read(self.reg[7])
        # Increment SP
        self.reg[7] += 1
        self.pc += 2

    # Step 11: Implement Subroutine Calls
    def ret_inst(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    # Step 11: Implement Subroutine Calls
    def call_inst(self):
        temp = self.ram_read(self.pc + 1)
        sub = self.reg[temp]

        ret = self.pc + 2
        while self.ram_read(ret) not in self.branch_table:
            ret += 1

        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret
        self.pc = sub

# Sprint Challenge
# Your finished project must include all of the following requirements:
#  Add the CMP instruction and equal flag to your LS-8.
#  Add the JMP instruction.
#  Add the JEQ and JNE instructions.

    def jmp_inst(self):
        # print("JMP")
        reg_a = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_a]

    def jeq_inst(self):
        # print("JEQ")
        if self.E == 1:
            self.jmp_inst()
        else:
            self.pc += 2

    def jne_inst(self):
        # print("JNE")
        if self.E == 0:
            self.jmp_inst()
        else:
            self.pc += 2

    def cmp_inst(self):
        # print("CMP")
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        if self.reg[reg_a] == self.reg[reg_b]:
            self.E = 1
        else:
            self.E = 0

        if self.reg[reg_a] < self.reg[reg_b]:
            self.L = 1
        else:
            self.L = 0

        if self.reg[reg_a] > self.reg[reg_b]:
            self.G = 1
        else:
            self.G = 0

        self.pc += 3


    def load(self, file):
        """Load a program into memory."""
        # Step 7: Un-hardcode the machine code
        # Make changes to cpu.py and ls8.py so that the program can be specified on the command line 
        # like so:
        # python3 ls8.py examples/mult.ls8

        address = 0

        # print(sys.argv)
        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#", 1)[0]
                        line = int(line, 2)
                        # print(value)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        # print(self.ram)

    def alu(self, op):
        """ALU operations."""
    # Stretch Problem
    # Add the ALU operations: AND OR XOR NOT SHL SHR MOD
 
        if op == "AND":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
            self.pc += 3

        elif op == "OR":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
            self.pc += 3

        elif op == "XOR":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
            self.pc += 3

        elif op == "NOT":
            reg_a = self.ram_read(self.pc + 1)
            self.reg[reg_a] = ~self.reg[reg_a]
            self.pc += 2

        elif op == "SHR":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
            self.pc += 3

        elif op == "SHL":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
            self.pc += 3

        elif op == "MOD":
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if self.reg[reg_b] == 0:
                self.hlt_inst()
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
            self.pc += 3

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

# Test
# if __name__ == "__main__":
#     LS8 = CPU()
#     LS8.load()
#     for i in range(9):
#         print(LS8.ram_read(i))
#     LS8.ram_write(0, 15)
#     print("==============")
#     print(LS8.ram_read(0))
#     print("==============")

# Day 1
# run the program and have it print 8 to the console!

# Day 2
# One you run it with python3 ls8.py examples/mult.ls8, you should see:
# 72

# Day 3
# If you run python3 ls8.py examples/stack.ls8 you should see the output:
# 2
# 4
# 1

# Day 4
# If you run python3 ls8.py examples/call.ls8 you should see the output:
# 20
# 30
# 36
# 60

# Day 5(Sprint)
# sctest should print:
# 1
# 4
# 5