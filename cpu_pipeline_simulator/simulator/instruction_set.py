import os

class InstructionSet:
    def __init__(self):
        self.instructions = {
            'ADD': {'type': 'R', 'exec_cycles': 1, 'uses_memory': False},
            'SUB': {'type': 'R', 'exec_cycles': 1, 'uses_memory': False},
            'MUL': {'type': 'R', 'exec_cycles': 3, 'uses_memory': False},
            'DIV': {'type': 'R', 'exec_cycles': 5, 'uses_memory': False},
            'AND': {'type': 'R', 'exec_cycles': 1, 'uses_memory': False},
            'OR': {'type': 'R', 'exec_cycles': 1, 'uses_memory': False},
            'XOR': {'type': 'R', 'exec_cycles': 1, 'uses_memory': False},
            'LW': {'type': 'I', 'exec_cycles': 2, 'uses_memory': True},
            'SW': {'type': 'I', 'exec_cycles': 2, 'uses_memory': True},
            'BEQ': {'type': 'I', 'exec_cycles': 1, 'uses_memory': False},
            'BNE': {'type': 'I', 'exec_cycles': 1, 'uses_memory': False},
            'JUMP': {'type': 'J', 'exec_cycles': 1, 'uses_memory': False},
            'JAL': {'type': 'J', 'exec_cycles': 1, 'uses_memory': False},
        }
    
    def parse_instruction(self, instr_str):
        """Parse an instruction string into components"""
        parts = instr_str.strip().split()
        op_code = parts[0]
        
        if op_code not in self.instructions:
            raise ValueError(f"Invalid instruction: {op_code}")
        
        instr_type = self.instructions[op_code]['type']
        operands = []
        
        if instr_type == 'R':  # Example: ADD R1, R2, R3
            operands = [p.strip(',') for p in parts[1:]]
        elif instr_type == 'I':  # Example: LW R1, 0(R2) or BEQ R1, R2, 100
            if op_code in ['LW', 'SW']:
                operands = [parts[1].strip(',')]
                # Parse memory reference like 0(R2)
                mem_ref = parts[2]
                offset = mem_ref.split('(')[0]
                reg = mem_ref.split('(')[1].strip(')')
                operands.extend([offset, reg])
            else:  # Branch instructions
                operands = [p.strip(',') for p in parts[1:]]
        elif instr_type == 'J':  # Example: JUMP 100
            operands = [parts[1]]
        
        return {
            'op_code': op_code,
            'type': instr_type,
            'operands': operands,
            'cycles': self.instructions[op_code]['exec_cycles'],
            'uses_memory': self.instructions[op_code]['uses_memory']
        }
    
    def extract_registers(self, instr_str):
        """Extract register names from an instruction string"""
        parsed = self.parse_instruction(instr_str)
        registers = []
        
        if parsed['type'] == 'R':  # Example: ADD R1, R2, R3
            registers = parsed['operands']
        elif parsed['type'] == 'I':
            if parsed['op_code'] in ['LW', 'SW']:
                registers = [parsed['operands'][0], parsed['operands'][2]]  # Dest/source and base registers
            else:  # Branch instructions
                registers = parsed['operands'][:2]  # First two operands are registers
        
        return registers
    
    def get_destination_register(self, instr_str):
        """Get the destination register of an instruction"""
        parsed = self.parse_instruction(instr_str)
        
        if parsed['type'] == 'R':  # Example: ADD R1, R2, R3
            return parsed['operands'][0]  # First operand is destination
        elif parsed['op_code'] == 'LW':  # Example: LW R1, 0(R2)
            return parsed['operands'][0]  # First operand is destination
        else:
            return None  # No destination register
    
    def get_source_registers(self, instr_str):
        """Get the source registers of an instruction"""
        parsed = self.parse_instruction(instr_str)
        
        if parsed['type'] == 'R':  # Example: ADD R1, R2, R3
            return parsed['operands'][1:]  # Second and third operands are sources
        elif parsed['op_code'] == 'LW':  # Example: LW R1, 0(R2)
            return [parsed['operands'][2]]  # Base register is source
        elif parsed['op_code'] == 'SW':  # Example: SW R1, 0(R2)
            return [parsed['operands'][0], parsed['operands'][2]]  # Value and base registers are sources
        elif parsed['op_code'] in ['BEQ', 'BNE']:  # Example: BEQ R1, R2, 100
            return parsed['operands'][:2]  # First two operands are sources
        else:
            return []
    
    def has_dependency(self, instr1, instr2):
        """Check if instr2 depends on instr1 (RAW hazard)"""
        dest_reg = self.get_destination_register(instr1)
        if not dest_reg:
            return False
            
        source_regs = self.get_source_registers(instr2)
        return dest_reg in source_regs
    
    def load_program(self, program_file):
        """Load a program from a file"""
        if not os.path.isfile(program_file):
            raise FileNotFoundError(f"Program file '{program_file}' not found.")
        
        with open(program_file, 'r') as f:
            self.program = [line.strip() for line in f if line.strip() and not line.startswith('#')]
