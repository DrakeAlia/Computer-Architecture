"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
         # pass

    # Create a 256 byts of memory and 8 general-purpose registers
    # Add PC program counter

        # Create 256 bites memory
        self.ram = [0b0] * 256
        # 8 bit register
        self.reg = [0] * 8
        # Program counter 
        self.pc = 0
        # reg 7 = 0xF4
        self.reg[7] = 0xF4


    def load(self):
        """Load a program into memory."""

        address = 0
        # For now, we've just hardcoded a program:
        # print(sys.argv)
        if len (sys.argv) > 1:
            filename = sys.argv[1]
            with open(
                filename
                # open('./examples/' + filename)
            ) as f: 
                address = 0
                for line in f:
                    value = line.split("#")[0].strip()
                    # print(value)
                    if value == "":
                        continue
                    else:
                        instruction = int(value, 2)
                        self.ram[address] = instruction
                        address += 1
        else:
            program = [
                # From print8.ls8
                0b10000010,  # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111,  # PRN R0
                0b00000000,
                0b00000001,  # HLT
            ]

            for address, instruction in enumerate(program):
                self.ram[address] = instruction

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    # Add ram methods

    # Ram read should accept the address to read and
    # Return the value stored there
    def ram_read(self, address):
        """prints content in specified address in RAM"""
        return self.ram[address]


    # Ram write should accept a value to write and the address to write it to
    def ram_write(self, value, address):
        """Overwrites ram with the value at specified address"""
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )
        for i in range(8):
            print(" %02X" % self.reg[i], end="")
        print()

    def run(self):
        """Run the CPU."""

        # Instructions
        HLT = 0b00000001 # Halt the CPU (and exit the emulator). 
        LDI = 0b10000010 # Set the value of a register to an integer.
        PRN = 0b01000111 # Print numeric value stored in the given register.
        MUL = 0b10100010 # Multiply the values in two registers together and store the result in registerA.
        ADD = 0b10100000  # Add the value in two registers and store the result in registerA.
        PUSH = 0b01000101 # Push the value in the given register on the stack.
        POP = 0b01000110 # Pop the value at the top of the stack into the given register.
        CALL = 0b01010000 # Calls a subroutine (function) at the address stored in the register.
        RET = 0b00010001 # Return from subroutine.
        NOP = 0b00000000 # No operation. Do nothing for this instruction.
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        SP = 7

        running = True

        while running:
            # Instructions register
            ir = self.ram[self.pc]
            # Operands
            # Register 1
            operand_a = self.ram[self.pc + 1]
            # Register 2
            operand_b = self.ram[self.pc + 2]

            # HLT
            if ir == HLT:
                running = False
                self.pc += 1

            # LDI
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                # Increment program counter by 3 steps inside the RAM
                self.pc += 3

            # PRN
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            # MUL
            elif ir == MUL:
                product = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = product
                self.pc += 3

            # PUSH
            elif ir == PUSH:
                # Decrement the stack pointer
                self.reg[SP] -= 1
                # Store value from reg to ram
                self.ram_write(self.reg[operand_a], self.reg[SP])
                self.pc += 2

            # POP
            elif ir == POP:
                # Read value of SP and overwrite next register
                value = self.ram_read(self.reg[SP])
                self.reg[operand_a] = value
                # Increment SP
                self.reg[SP] += 1
                self.pc += 2

            # ADD
            elif ir == ADD:
                add = self.reg[operand_a] + self.reg[operand_b]
                self.reg[operand_a] = add
                self.pc += 3

            # NOP
            elif ir == NOP:
                # Do nothing and procced to the next instruction
                self.pc += 1
                continue

            # CALL 
            elif ir == CALL:
                self.reg[SP] -= 1
                self.ram_write(self.pc + 2, self.reg[SP])
                self.pc = self.reg[operand_a]

            # RET
            elif ir == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1

            # CMP
            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            # JMP
            elif ir == JMP:
                self.pc == self.reg[operand_a]
                break

            # JEQ
            elif ir == JEQ:
                if (self.flag & HLT) == 1:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            # JNE
            elif ir == JNE:
                if (self.flag & HLT) == 0:
                    self.pc = self.reg[operand_a]

                else:
                    self.pc += 2

            # Unknown instructions
            else:
                print(f"Unknown instruction {ir} at address {self.pc}")
                self.pc += 1

# Test
if __name__ == "__main__":
    LS8 = CPU()
    LS8.load()
    for i in range(9):
        print(LS8.ram_read(i))
    LS8.ram_write(0, 15)
    print("==============")
    print(LS8.ram_read(0))
    print("==============")