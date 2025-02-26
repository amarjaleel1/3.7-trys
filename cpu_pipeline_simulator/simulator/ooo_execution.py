"""
Out-of-Order Execution implementation for the CPU Pipeline Simulator.
Includes reservation stations, reorder buffer, and register renaming.
"""

class ReservationStation:
    """Reservation station for holding instructions waiting for operands"""
    
    def __init__(self, id, capacity=8):
        self.id = id
        self.capacity = capacity
        self.entries = [None] * capacity
    
    def is_full(self):
        """Check if the reservation station is full"""
        return None not in self.entries
    
    def add_instruction(self, instruction, op1_ready, op1_value=None, op1_tag=None, 
                        op2_ready=False, op2_value=None, op2_tag=None):
        """Add an instruction to the reservation station"""
        if self.is_full():
            return False
        
        # Find an empty slot
        for i in range(self.capacity):
            if self.entries[i] is None:
                self.entries[i] = {
                    'instruction': instruction,
                    'op1_ready': op1_ready,
                    'op1_value': op1_value,
                    'op1_tag': op1_tag,
                    'op2_ready': op2_ready,
                    'op2_value': op2_value,
                    'op2_tag': op2_tag,
                    'executing': False,
                    'complete': False
                }
                return True
        
        return False
    
    def update_operand(self, tag, value):
        """Update operands in all waiting instructions when a result becomes available"""
        for entry in self.entries:
            if entry is None:
                continue
            
            # Update first operand if waiting for this tag
            if not entry['op1_ready'] and entry['op1_tag'] == tag:
                entry['op1_ready'] = True
                entry['op1_value'] = value
                entry['op1_tag'] = None
            
            # Update second operand if waiting for this tag
            if not entry['op2_ready'] and entry['op2_tag'] == tag:
                entry['op2_ready'] = True
                entry['op2_value'] = value
                entry['op2_tag'] = None
    
    def get_ready_instructions(self):
        """Get instructions that are ready to execute"""
        ready = []
        for i, entry in enumerate(self.entries):
            if entry is not None and not entry['executing'] and not entry['complete'] and \
                entry['op1_ready'] and entry['op2_ready']:
                ready.append((i, entry))
        return ready
    
    def mark_executing(self, index):
        """Mark an instruction as currently executing"""
        if 0 <= index < self.capacity and self.entries[index] is not None:
            self.entries[index]['executing'] = True
    
    def mark_complete(self, index):
        """Mark an instruction as complete"""
        if 0 <= index < self.capacity and self.entries[index] is not None:
            self.entries[index]['executing'] = False
            self.entries[index]['complete'] = True
    
    def remove_instruction(self, index):
        """Remove an instruction from the reservation station"""
        if 0 <= index < self.capacity:
            self.entries[index] = None

class ReorderBuffer:
    """Reorder buffer for maintaining in-order commit of out-of-order execution"""
    
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.entries = [None] * capacity
        self.head = 0  # Oldest instruction
        self.tail = 0  # Next free slot
        self.size = 0
    
    def is_full(self):
        """Check if the reorder buffer is full"""
        return self.size == self.capacity
    
    def is_empty(self):
        """Check if the reorder buffer is empty"""
        return self.size == 0
    
    def add_instruction(self, instruction, destination=None):
        """Add an instruction to the reorder buffer"""
        if self.is_full():
            return -1  # No space in ROB
        
        # Assign entry
        rob_id = self.tail
        self.entries[rob_id] = {
            'instruction': instruction,
            'destination': destination,
            'value': None,
            'ready': False
        }
        
        # Update tail and size
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1
        
        return rob_id
    
    def update_result(self, rob_id, value):
        """Update the result of an instruction in the reorder buffer"""
        if 0 <= rob_id < self.capacity and self.entries[rob_id] is not None:
            self.entries[rob_id]['value'] = value
            self.entries[rob_id]['ready'] = True
    
    def commit_next(self):
        """Commit the next instruction in order"""
        if self.is_empty() or not self.entries[self.head]['ready']:
            return None
        
        # Get the entry to commit
        entry = self.entries[self.head]
        result = (entry['instruction'], entry['destination'], entry['value'])
        
        # Clear the entry and update head and size
        self.entries[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        
        return result

class RegisterRenaming:
    """Register renaming to eliminate WAW and WAR hazards"""
    
    def __init__(self, num_arch_regs=32, num_phys_regs=64):
        self.num_arch_regs = num_arch_regs
        self.num_phys_regs = num_phys_regs
        
        # Register mapping table (arch_reg -> phys_reg)
        self.register_map = {f"R{i}": i for i in range(num_arch_regs)}
        
        # Register availability
        self.is_available = [True] * num_phys_regs
        
        # Initialize first num_arch_regs as mapped
        for i in range(num_arch_regs):
            self.is_available[i] = False
        
        # Register alias table (phys_reg -> value)
        self.register_values = [0] * num_phys_regs
        
        # Register status (waiting or ready)
        self.register_ready = [True] * num_phys_regs
    
    def allocate_register(self, arch_reg):
        """Allocate a physical register for an architectural register"""
        # Find a free physical register
        for phys_reg in range(self.num_phys_regs):
            if self.is_available[phys_reg]:
                # Allocate this register
                self.is_available[phys_reg] = False
                old_phys_reg = self.register_map[arch_reg]
                self.register_map[arch_reg] = phys_reg
                self.register_ready[phys_reg] = False
                
                return phys_reg, old_phys_reg
        
        return -1, -1  # No free physical registers
    
    def get_register_mapping(self, arch_reg):
        """Get the physical register mapped to an architectural register"""
        return self.register_map.get(arch_reg, -1)
    
    def is_register_ready(self, phys_reg):
        """Check if a physical register's value is ready"""
        if 0 <= phys_reg < self.num_phys_regs:
            return self.register_ready[phys_reg]
        return False
    
    def get_register_value(self, phys_reg):
        """Get the value of a physical register"""
        if 0 <= phys_reg < self.num_phys_regs:
            return self.register_values[phys_reg]
        return 0
    
    def set_register_value(self, phys_reg, value):
        """Set the value of a physical register and mark it ready"""
        if 0 <= phys_reg < self.num_phys_regs:
            self.register_values[phys_reg] = value
            self.register_ready[phys_reg] = True
    
    def free_register(self, phys_reg):
        """Free a physical register when it's no longer needed"""
        if 0 <= phys_reg < self.num_phys_regs:
            self.is_available[phys_reg] = True

class OutOfOrderExecutionEngine:
    """Out-of-order execution engine using Tomasulo's algorithm"""
    
    def __init__(self, processor):
        self.processor = processor
        self.reservation_stations = {
            'int': ReservationStation('Integer', 8),
            'mul': ReservationStation('Multiply', 4),
            'load': ReservationStation('Load', 6),
            'store': ReservationStation('Store', 6)
        }
        self.rob = ReorderBuffer(16)
        self.register_renaming = RegisterRenaming()
        
        # Functional units
        self.functional_units = {
            'int': {'count': 2, 'busy': [False, False], 'cycles': 1},
            'mul': {'count': 1, 'busy': [False], 'cycles': 4},
            'load': {'count': 2, 'busy': [False, False], 'cycles': 2},
            'store': {'count': 1, 'busy': [False], 'cycles': 2}
        }
        
        # Instructions currently being executed
        self.executing_instructions = []
        
        # Statistics
        self.issued = 0
        self.executed = 0
        self.committed = 0
    
    def issue_instruction(self, instruction):
        """Issue an instruction to the appropriate reservation station"""
        # Parse instruction
        from simulator.instruction_set import InstructionSet
        instr_set = InstructionSet()
        parsed = instr_set.parse_instruction(instruction)
        
        # Determine reservation station type
        rs_type = self._get_rs_type(parsed['op_code'])
        
        # Check if ROB and reservation station have space
        if self.rob.is_full() or self.reservation_stations[rs_type].is_full():
            return False
        
        # Register renaming and operand fetching
        dest_reg = None
        op1_ready = True
        op1_value = 0
        op1_tag = None
        op2_ready = True
        op2_value = 0
        op2_tag = None
        
        if parsed['type'] == 'R':
            # R-type: ADD R1, R2, R3 -> R1 = R2 + R3
            dest_reg = parsed['operands'][0]
            src1_reg = parsed['operands'][1]
            src2_reg = parsed['operands'][2]
            
            # Map source registers
            src1_phys = self.register_renaming.get_register_mapping(src1_reg)
            src2_phys = self.register_renaming.get_register_mapping(src2_reg)
            
            # Check if operands are ready
            op1_ready = self.register_renaming.is_register_ready(src1_phys)
            op2_ready = self.register_renaming.is_register_ready(src2_phys)
            
            if op1_ready:
                op1_value = self.register_renaming.get_register_value(src1_phys)
            else:
                op1_tag = src1_phys
                
            if op2_ready:
                op2_value = self.register_renaming.get_register_value(src2_phys)
            else:
                op2_tag = src2_phys
                
            # Allocate destination register
            dest_phys, old_dest_phys = self.register_renaming.allocate_register(dest_reg)
            
        elif parsed['op_code'] == 'LW':
            # LW R1, 100(R2) -> R1 = MEM[R2+100]
            dest_reg = parsed['operands'][0]
            offset = int(parsed['operands'][1])
            base_reg = parsed['operands'][2]
            
            # Map source register
            base_phys = self.register_renaming.get_register_mapping(base_reg)
            
            # Check if base register is ready
            op1_ready = self.register_renaming.is_register_ready(base_phys)
            if op1_ready:
                op1_value = self.register_renaming.get_register_value(base_phys) + offset
            else:
                op1_tag = base_phys
                
            op2_ready = True  # No second operand for load
            
            # Allocate destination register
            dest_phys, old_dest_phys = self.register_renaming.allocate_register(dest_reg)
            
        elif parsed['op_code'] == 'SW':
            # SW R1, 100(R2) -> MEM[R2+100] = R1
            src_reg = parsed['operands'][0]
            offset = int(parsed['operands'][1])
            base_reg = parsed['operands'][2]
            
            # Map source registers
            src_phys = self.register_renaming.get_register_mapping(src_reg)
            base_phys = self.register_renaming.get_register_mapping(base_reg)
            
            # Check if operands are ready
            op1_ready = self.register_renaming.is_register_ready(src_phys)
            op2_ready = self.register_renaming.is_register_ready(base_phys)
            
            if op1_ready:
                op1_value = self.register_renaming.get_register_value(src_phys)
            else:
                op1_tag = src_phys
                
            if op2_ready:
                op2_value = self.register_renaming.get_register_value(base_phys) + offset
            else:
                op2_tag = base_phys
                
            dest_reg = None  # No destination register
            
        else:
            # Handle branches and jumps
            pass
        
        # Add to reorder buffer
        rob_id = self.rob.add_instruction(instruction, dest_reg)
        if rob_id < 0:
            return False
            
        # Add to reservation station
        success = self.reservation_stations[rs_type].add_instruction(
            instruction, op1_ready, op1_value, op1_tag, op2_ready, op2_value, op2_tag
        )
        
        if success:
            self.issued += 1
            return True
        else:
            # If reservation station is full, need to recover
            # This should not happen as we checked earlier, but just in case
            return False
    
    def execute_cycle(self):
        """Execute a single cycle of the out-of-order execution engine"""
        # 1. Check for instructions that can begin execution
        self._start_execution()
        
        # 2. Continue execution of in-progress instructions
        self._continue_execution()
        
        # 3. Write results of completed instructions
        self._write_results()
        
        # 4. Commit instructions in order
        self._commit_instructions()
        
        return True
    
    def _get_rs_type(self, op_code):
        """Get the reservation station type for an operation"""
        if op_code in ['MUL', 'DIV']:
            return 'mul'
        elif op_code == 'LW':
            return 'load'
        elif op_code == 'SW':
            return 'store'
        else:
            return 'int'
    
    def _start_execution(self):
        """Start execution of ready instructions if functional units are available"""
        for rs_type, rs in self.reservation_stations.items():
            # Get instructions ready to execute
            ready_instructions = rs.get_ready_instructions()
            
            # Check if functional unit is available
            fu = self.functional_units[rs_type]
            for i in range(fu['count']):
                if not fu['busy'][i] and ready_instructions:
                    # Start executing the instruction
                    index, entry = ready_instructions.pop(0)
                    rs.mark_executing(index)
                    fu['busy'][i] = True
                    
                    # Add to executing instructions
                    self.executing_instructions.append({
                        'rs_type': rs_type,
                        'rs_index': index,
                        'fu_index': i,
                        'instruction': entry['instruction'],
                        'op1_value': entry['op1_value'],
                        'op2_value': entry['op2_value'],
                        'cycles_left': fu['cycles']
                    })
    
    def _continue_execution(self):
        """Continue execution of in-progress instructions"""
        for instr in self.executing_instructions:
            instr['cycles_left'] -= 1
    
    def _write_results(self):
        """Write results of completed instructions"""
        completed = []
        for i, instr in enumerate(self.executing_instructions):
            if instr['cycles_left'] <= 0:
                # Execution completed
                rs_type = instr['rs_type']
                rs_index = instr['rs_index']
                fu_index = instr['fu_index']
                
                # Mark reservation station entry as complete
                self.reservation_stations[rs_type].mark_complete(rs_index)
                
                # Free functional unit
                self.functional_units[rs_type]['busy'][fu_index] = False
                
                # For now, just a placeholder result - in a real implementation we'd calculate the actual result
                result_value = instr['op1_value'] + instr['op2_value']
                
                # TODO: Update ROB with result
                
                # Mark for removal
                completed.append(i)
                self.executed += 1
        
        # Remove completed instructions from executing list
        for i in reversed(completed):
            self.executing_instructions.pop(i)
    
    def _commit_instructions(self):
        """Commit completed instructions in order"""
        result = self.rob.commit_next()
        if result:
            instruction, dest_reg, value = result
            if dest_reg:
                # Update architectural state
                self.processor.write_register(dest_reg, value)
            self.committed += 1
            return True
        return False
    
    def stats(self):
        """Return statistics about the out-of-order execution engine"""
        return {
            'issued': self.issued,
            'executed': self.executed,
            'committed': self.committed,
            'rob_size': self.rob.size,
            'rob_capacity': self.rob.capacity,
            'executing': len(self.executing_instructions)
        }
