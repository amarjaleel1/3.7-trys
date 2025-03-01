import os

class Processor:
    def __init__(self):
        # Initialize registers (R0-R31)
        self.registers = {f"R{i}": 0 for i in range(32)}
        # R0 is always 0 in many architectures
        self.registers["R0"] = 0
        
        # Program Counter
        self.pc = 0
        
        # Memory (simple dictionary implementation)
        self.memory = {}
        
        # Initialize some memory values for testing
        for i in range(100):
            self.memory[i] = i * 10
    
    def read_register(self, reg_name):
        """Read value from register"""
        if reg_name in self.registers:
            return self.registers[reg_name]
        else:
            raise ValueError(f"Invalid register name: {reg_name}")
    
    def write_register(self, reg_name, value):
        """Write value to register"""
        if reg_name in self.registers and reg_name != "R0":
            self.registers[reg_name] = value
        elif reg_name == "R0":
            # R0 is always 0 in many architectures
            pass
        else:
            raise ValueError(f"Invalid register name: {reg_name}")
    
    def read_memory(self, address):
        """Read value from memory"""
        if address in self.memory:
            return self.memory[address]
        else:
            # Initialize uninitialized memory to 0
            self.memory[address] = 0
            return 0
    
    def write_memory(self, address, value):
        """Write value to memory"""
        self.memory[address] = value
    
    def execute_alu(self, operation, operand1, operand2):
        """Execute ALU operation"""
        if operation == "ADD":
            return operand1 + operand2
        elif operation == "SUB":
            return operand1 - operand2
        elif operation == "MUL":
            return operand1 * operand2
        elif operation == "DIV":
            return operand1 // operand2 if operand2 != 0 else 0
        elif operation == "AND":
            return operand1 & operand2
        elif operation == "OR":
            return operand1 | operand2
        elif operation == "XOR":
            return operand1 ^ operand2
        else:
            raise ValueError(f"Unsupported ALU operation: {operation}")
    
    def load_program(self, program_file):
        """Load a program from a file"""
        if not os.path.isfile(program_file):
            raise FileNotFoundError(f"Program file '{program_file}' not found.")
        
        with open(program_file, 'r') as f:
            self.program = [line.strip() for line in f if line.strip() and not line.startswith('#')]
