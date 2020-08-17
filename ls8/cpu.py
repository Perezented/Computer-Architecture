
"""CPU functionality."""


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        print('Welcome, Now booting up Janky OS')

        self.reg = [0] * 8

    def ram_read(self, location):
        return self.ram[location]

    def ram_write(self, value, location,):
        self.ram[location] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]
        self.pc = 0
        self.ram = [0]*255
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):

        self.trace()
        # print(self.load())
        print(f'Total reg: {self.reg} ')
        print(f'Total RAM: {self.ram}')
        print(f'Your pc: {self.pc}')

        running = True
        while running:

            ir = self.ram[self.pc]
            # print(self.reg, self.pc)
            print(f'Current IR: {ir}')

            if ir == 1:  # HLT -- Computer Halt (STOP)
                print('COMPUTER STOPPED')
                running = False
                self.pc += 1
            if ir == 130:   # LDI -- Add following item to ram
                print(f' in LDI, self.pc: {self.pc} ')
                self.pc += 3
            if ir == 71:    # PRN -- Display next item from ram
                print(self.pc, self.pc + 1, self.pc + 2)
                print(self.ram[self.pc])
                print(self.ram[self.pc+1])
                print(self.ram[self.pc+2])
                self.ram_read(self.pc+1)
                print(f'self.ram_read(self.pc+1): {self.ram_read(self.pc+2)} ')
                self.pc += 2
