# Bitwise Operations
# ------------------
# First, Boolean.
# A  B    A and B
# ---------------
# F  F       F
# F  T       F
# T  F       F
# T  T       T
# A  B     A OR B
# ---------------
# F  F       F
# F  T       T
# T  F       T
# T  T       T
# A   NOT A
# ---------
# T     F
# F     T
# Then, bitwise:
# A  B     A & B  (bitwise AND)
# ---------------
# 0  0       0
# 0  1       0
# 1  0       0
# 1  1       1
# A  B     A | B  (bitwise OR)
# ---------------
# 0  0       0
# 0  1       1
# 1  0       1
# 1  1       1
# A   ~A  (bitwise NOT)
# ------
# 1    0
# 0    1
#   1100
# & 0110
# ------
#   0100
#        vvvvvvv
#   101101100110101
# & 000001111111000    "AND masking", stencil
# -----------------
#   000001100110000
#        ^^^^^^^
# Bitwise AND can mask out parts of a number, or clear individual bits of a number to 0.
# Bitwise OR can set individual bits (or groups of bits) to 1
#   00011011000
# | 11111100000
# -------------
#   11111111000
# Bit shifting
# ------------
# 10101011
# 01010101
# 00101010
# 00010101
# 00001010
# 00000101
# 00000010
# 00000001
# 00000000
# Analogy in Base 10 of extracting numbers
# ----------------------------------------
#   vv
# 1234567
# 0123456  shift 3 right  (AKA // 1000)
# 0012345
# 0001234
#      ^^
# 0000034  mask out the 34
# Now in Binary
# -------------
#    vvvv
# 0101001010110
# 0101001010110  Shift right by 6
#  010100101011
#   01010010101
#    0101001010
#     010100101
#      01010010
#       0101001
#          ^^^^
#       0101t01
#     & 0001111  Mask the result
#     ---------
#       0001001
#          ^^^^
# If n is a power of 2:
#    x % n
#    is the same as
#    x & (n - 1)


import sys
​
# The index into the memory array, AKA location, address, pointer
​
# 1 - PRINT_BEEJ
# 2 - HALT
# 3 - SAVE_REG  store a value in a register
# 4 - PRINT_REG  print the register value in decimal
​
memory = [0] * 256   # think of as a big array of bytes, 8-bits per byte
​
registers = [0] * 8
​
# Load the program file
address = 0
​
if len(sys.argv) != 2:
	print("usage: comp.py progname")
	sys.exit(1)
​
try:
	with open(sys.argv[1]) as f:
		for line in f:
			line = line.strip()
			temp = line.split()
​
			if len(temp) == 0:
				continue
​
			if temp[0][0] == '#':
				continue
​
			try:
				memory[address] = int(temp[0])
​
			except ValueError:
				print(f"Invalid number: {temp[0]}")
				sys.exit(1)
​
			address += 1
​
except FileNotFoundError:
	print(f"Couldn't open {sys.argv[1]}")
	sys.exit(2)
​
if address == 0:
	print("Program was empty!")
	sys.exit(3)
​
#print(memory[:10])
#sys.exit(0)
​
​
running = True
​
pc = 0   # Program Counter, the index into memory of the currently-executing instruction
​
while running:
	ir = memory[pc]  # Instruction Register
​
	if ir == 1:  # PRINT_BEEJ
		print("Beej!")
		pc += 1
​
	elif ir == 2:  # HALT
		running = False
		pc += 1
​
	elif ir == 3:  # SAVE_REG
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		registers[reg_num] = value
​
		pc += 3
​
	elif ir == 4:  # PRINT_REG
		reg_num = memory[pc + 1]
		print(registers[reg_num])
​
		pc += 2
​
	else:
		print(f"Invalid instruction {ir} at address {pc}")
		sys.exit(1)



# Hi!
​
1  # PRINT_BEEJ
   
3  # SAVE_REG R4 37, instruction itself also called "opcode"
4  # 4 and 37 are arguments to SAVE_REG, also called "operands"
37
​
4  # PRINT_REG R4
4
​
2   # HALT