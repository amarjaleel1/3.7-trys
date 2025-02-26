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
    
    # ...existing code...

# Make sure to export Pipeline class - THIS IS IMPORTANT
__all__ = ['Pipeline', 'PipelineStage']
