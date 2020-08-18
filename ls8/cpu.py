import sys

"""CPU functionality."""


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        print('Welcome, Now booting up Janky OS')
        self.pc = 0
        self.ram = [0]*255
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""
        program = []
        print(sys.argv)

        load_file = sys.argv[1]
        with open(load_file, 'r') as f:
            for line in f:
                # print(line)
                if line[0] == '\n' or line[0] == '#' or len(line) == 0:
                    continue
                else:
                    print(line[:8])
                    program.append(int(line[:8], 2))

            # i = 0
            # eight = ''
            # while i != len(lines):
            #     if lines[i] == '1' or lines[i] == '0':
            #         if len(eight) != 8:
            #             # print(lines[i])
            #             eight = eight + lines[i]
            #             # print(eight)
            #         else:
            #             print(eight)
            #             program.append(bin(int(eight)))
            #             eight = ''

            #     i += 1
            # print(eight)
            print(program)
            # print(lines)
            f.close()

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     # 0b10000010,  # LDI R0,8
        #     # 0b00000000,
        #     # 0b00001000,
        #     # 0b01000111,  # PRN R0
        #     # 0b00000000,
        #     # 0b00000001,  # HLT
        # ]

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

    def ram_read(self, address):
        # print(address, self.ram)
        # print(self.ram[address])
        self.reg[0] = self.ram[address]
        print(self.ram[self.reg[0]])
        return self.ram[self.reg[0]]

    def ram_write(self, address, item):
        # print(address, self.ram[address])
        # print(item, self.ram[item])
        self.reg[1] = self.ram[item]
        self.reg[0] = self.ram[address]
        # print(self.reg)
        self.ram[self.reg[0]] = self.reg[1]
        return self.ram

    def run(self):

        self.trace()
        # print(self.load())
        print(f'Total reg: {self.reg} ')
        print(f'Total RAM: {self.ram}')

        running = True
        while running:
            ir = self.ram[self.pc]
            # print(f'Current IR: {ir}')

            if ir == 1:  # HLT -- Computer Halt (STOP)
                print(f'{"-"*10} HLT {"-"*10} ')
                print('COMPUTER STOPPED')
                running = False
                self.pc += 1

            if ir == 130:  # LDI -- Add following item to ram
                print(f'{"-"*10} LDI {"-"*10} ')
                # print(f' in LDI, self.pc: {self.pc} ')
                # print(self.reg)
                self.ram_write(self.pc+1, self.pc+2)
                self.pc += 3

            if ir == 71:    # PRN -- Display next item from ram
                print(f'{"-"*10} PRN {"-"*10} ')
                # print(f' in PRN, self.pc: {self.pc} ')
                self.ram_read(self.pc+1)
                # print(self.ram)
                self.pc += 2
