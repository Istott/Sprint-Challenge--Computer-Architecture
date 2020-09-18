import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.address = 0
        self.ram = [0] * 256
        self.reg = [0] * 98
        self.pc = 0
        self.sp = 7
        self.flag = 0b00000000 # null
        self.LDI = 0b10000010 # 128 + 2 = 130
        self.PRN = 0b01000111 # 64 + 4 + 2 + 1 = 71
        self.HLT = 0b00000001 # 1
        self.ADD = 0b10100000 # 128 + 32 = 160
        self.MUL = 0b10100010 # 128 + 32 + 2 = 162
        self.PUSH = 0b01000101 # 64 + 4 + 1 = 69
        self.POP = 0b01000110 # 64 + 4 + 2 = 70
        self.CALL = 0b01010000 # 64 + 16 = 80
        self.RET = 0b00010001 # 16 + 1 = 17
        self.CMP = 0b10100111 # 128 + 32 + 4 + 2 + 1 = 167
        self.JMP = 0b01010100 # 64 + 16 + 4 + = 84
        self.JEQ = 0b01010101 # 64 + 16 + 4 + 1 = 85
        self.JNE = 0b01010110 # 64 + 16 + 4 + 2 = 86


    def ram_read(self, address = None):
        return self.ram[address]
    
    def ram_write(self, value = None, address = None):
        self.ram[address] = value
        return self.ram[address]

    def load(self, filename):
        """Load a program into memory."""

        with open(filename) as f:

            for val in f:

                val = val.strip().split("#", 1)[0]

                if val == '':
                    continue

                val = int(val, 2)
                self.ram[self.address] = val
                self.address += 1

                if len(sys.argv) != 2:
                    print("Expected Usage: ls8.py [filename-to-run]")
                    sys.exit(1)

                if ValueError:
                    pass


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.flag,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.reg[self.sp] = 0xf4
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == self.PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == self.HLT:
                running = False

            elif IR == self.ADD:
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
                print('ADD')

            elif IR == self.MUL:
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
                print('MUL')

            elif IR == self.PUSH:
                self.reg[self.sp] -= 1
                self.reg[self.sp] &= 0xff
                num = self.ram[self.pc + 1]
                value = self.reg[num]
                push_to = self.reg[self.sp]
                self.ram[push_to] = value
                self.pc += 2

            elif IR == self.POP:
                pop_from = self.reg[self.sp]
                value = self.ram[pop_from]
                num = self.ram[self.pc + 1]
                self.reg[num] = value
                self.reg[self.sp] += 1
                self.pc += 2

            elif IR == self.CALL:
                return_address = self.pc + 2
                self.reg[self.sp] -= 1
                push_to = self.reg[self.sp]
                self.ram[push_to] = return_address
                num = self.ram[self.pc + 1]
                sub_address = self.reg[num]
                self.pc = sub_address

            elif IR == self.RET:
                pop_from = self.reg[self.sp]
                return_address = self.ram[pop_from]
                self.reg[self.sp] += 1
                self.pc = return_address

            elif IR == self.CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.flag = 0b00000001

                elif self.reg[operand_a] > self.reg[operand_b]:
                    self.flag = 0b00000010

                else:
                    self.flag = 0b00000000

                self.pc += 3

            elif IR == self.JMP:
                self.address = self.reg[self.ram[self.pc + 1]]
                self.pc = self.address

            elif IR == self.JEQ:
                if self.flag == 0b00000001:
                    self.address = self.reg[self.ram[self.pc + 1]]
                    self.pc = self.address

                else:
                    self.pc += 2

            elif IR == self.JNE:
                if self.flag == 0b00000000:
                    self.address = self.reg[self.ram[self.pc + 1]]
                    self.pc = self.address

                else:
                    self.pc += 2           

            else:
                running = False
                print(f"{IR} not found")

