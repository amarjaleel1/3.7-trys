import os
import sys
from cpu_pipeline_simulator.simulator.processor import Processor
from cpu_pipeline_simulator.simulator.instruction_set import InstructionSet

class PipelineStage:
    def __init__(self, name):
        self.name = name
        self.instruction = None
        self.busy = False
        self.stall = False
        
    def execute(self):
        """Execute the current instruction in this stage"""
        if self.instruction and not self.stall:
            print(f"Executing {self.instruction} in {self.name} stage")
            return True
        return False
    
    def is_free(self):
        """Check if stage can accept new instruction"""
        return not self.busy and not self.stall

class Pipeline:
    def __init__(self, processor, instruction_set):
        self.processor = processor
        self.instruction_set = instruction_set
        self.cycles = 0
        self.stalls = 0
        self.hazards = {'data': 0, 'control': 0, 'structural': 0}
        self.verbose = True  # Default to verbose output
        
        # Define pipeline stages
        self.stages = {
            'fetch': PipelineStage('Fetch'),
            'decode': PipelineStage('Decode'),
            'execute': PipelineStage('Execute'),
            'memory': PipelineStage('Memory'),
            'writeback': PipelineStage('Writeback')
        }
        
        self.program = []
        self.pc = 0  # Program counter
        
        # Add branch prediction status
        self.branch_prediction_enabled = False
        self.branch_predictions = {'correct': 0, 'incorrect': 0}
    
    def load_program(self, program_file):
        """Load a program from a file"""
        if not os.path.isfile(program_file):
            raise FileNotFoundError(f"Program file '{program_file}' not found.")
        
        with open(program_file, 'r') as f:
            self.program = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    def load_test_program(self):
        """Load a default test program"""
        self.program = [
            "ADD R1, R0, 10",
            "ADD R2, R0, 5",
            "MUL R3, R1, R2",
            "SUB R4, R3, R2",
            "DIV R5, R4, R1"
        ]
    
    def run(self):
        """Run the pipeline simulation"""
        while self.pc < len(self.program) or any(stage.instruction for stage in self.stages.values()):
            self.cycles += 1
            
            # Execute stages in reverse order to avoid overwriting
            self._execute_writeback()
            self._execute_memory()
            self._execute_execute()
            self._execute_decode()
            self._execute_fetch()
            
            # Check for hazards
            if self.check_hazards():
                self.stalls += 1
            
            if self.verbose:
                self.print_pipeline_state()
    
    def _execute_fetch(self):
        """Fetch stage"""
        stage = self.stages['fetch']
        if stage.is_free() and self.pc < len(self.program):
            stage.instruction = self.program[self.pc]
            stage.busy = True
            self.pc += 1
    
    def _execute_decode(self):
        """Decode stage"""
        stage = self.stages['decode']
        fetch_stage = self.stages['fetch']
        if stage.is_free() and fetch_stage.busy:
            stage.instruction = fetch_stage.instruction
            stage.busy = True
            fetch_stage.busy = False
    
    def _execute_execute(self):
        """Execute stage"""
        stage = self.stages['execute']
        decode_stage = self.stages['decode']
        if stage.is_free() and decode_stage.busy:
            stage.instruction = decode_stage.instruction
            stage.busy = True
            decode_stage.busy = False
    
    def _execute_memory(self):
        """Memory stage"""
        stage = self.stages['memory']
        execute_stage = self.stages['execute']
        if stage.is_free() and execute_stage.busy:
            stage.instruction = execute_stage.instruction
            stage.busy = True
            execute_stage.busy = False
    
    def _execute_writeback(self):
        """Writeback stage"""
        stage = self.stages['writeback']
        memory_stage = self.stages['memory']
        if stage.is_free() and memory_stage.busy:
            stage.instruction = memory_stage.instruction
            stage.busy = True
            memory_stage.busy = False
    
    def check_hazards(self):
        """Check for hazards in the pipeline"""
        # Placeholder for hazard detection logic
        return False
    
    def print_pipeline_state(self):
        """Print the current state of the pipeline"""
        print(f"Cycle {self.cycles}:")
        for stage_name, stage in self.stages.items():
            status = "STALLED" if stage.stall else "BUSY" if stage.busy else "IDLE"
            instr = stage.instruction if stage.instruction else "NOP"
            print(f"{stage_name.upper()}: {status} - {instr}")
        print("-" * 40)

# Make sure to export Pipeline class - THIS IS IMPORTANT
__all__ = ['Pipeline', 'PipelineStage']
