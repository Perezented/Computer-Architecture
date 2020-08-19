"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        program = []
        if len(sys.argv) == 1:

            sys.argv.append(
                'c:\\Users\\MPere\\Desktop\\Lambda\\Python\\Computer-Architecture\\ls8\\examples\\mult.ls8')
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

            # print(program)
            f.close()

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
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
        """Run the CPU."""
        self.trace()

        running = True
        while running:
            ir = self.ram_read(self.pc)
            print(f'Current IR: {ir}')

            if ir == 1:  # HLT -- Computer Halt (STOP)
                print(f'{"-"*10} HLT {"-"*10} ')
                print('COMPUTER STOPPED')
                running = False
                self.pc += 1

            if ir == 0b10000010:  # LDI -- Add following item to reg???
                print(f'{"-"*10} LDI {"-"*10} ')
                print(self.pc, self.reg, self.ram)
                self.reg[self.ram_read(self.pc + 1)
                         ] = self.ram_read(self.pc + 2)

                self.pc += 3

            if ir == 71:    # PRN -- Display next item from ram
                print(self.reg[self.ram_read(self.pc + 1)])

                self.pc += 2

            if ir == 0b10100010:   # MUL -- multipy the next two
                print(f'{"-"*10} MUL {"-"*10} ')
                print(f'current ram: {self.ram, self.pc}')
                print(self.reg)
                self.alu('MUL', self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

    def ram_read(self, address):
        # print(self.ram[address])
        return self.ram[address]

    def ram_write(self, address, item):
        print('in ram_write')
        print(address, item)
        self.ram[address] = item

    def reg_write(self, address, item):
        self.reg[address] = item

    def reg_read(self, address):
        print(self.reg[address])
        return self.reg[address]


"""Main."""


cpu = CPU()

cpu.load()
cpu.run()
