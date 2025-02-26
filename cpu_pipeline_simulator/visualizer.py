import os
import sys
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init()

# Add the project directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from simulator.pipeline import Pipeline

class PipelineVisualizer:
    """Visualizes the state of the CPU pipeline"""
    
    def __init__(self, pipeline):
        """Initialize with a pipeline instance"""
        self.pipeline = pipeline
        self.history = []
        self.pipeline.visualizer = self
        
    def record_state(self):
        """Record the current state of the pipeline"""
        state = {}
        for stage_name, stage in self.pipeline.stages.items():
            state[stage_name] = {
                'instruction': stage.instruction,
                'busy': stage.busy,
                'stall': stage.stall
            }
        state['cycle'] = self.pipeline.cycles
        state['pc'] = self.pipeline.pc
        self.history.append(state)
    
    def print_horizontal_view(self):
        """Print a horizontal view of the pipeline"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"CPU Pipeline Simulator - Cycle {self.pipeline.cycles}")
        print("=" * 80)

        # Print the current state of each stage
        print("Pipeline Stages:")
        stage_names = ['fetch', 'decode', 'execute', 'memory', 'writeback']
        for stage_name in stage_names:
            stage = self.pipeline.stages[stage_name]
            status = "STALLED" if stage.stall else "BUSY" if stage.busy else "IDLE"
            color = Fore.RED if stage.stall else Fore.YELLOW if stage.busy else Fore.GREEN
            instr = stage.instruction if stage.instruction else "NOP"
            print(f"{Fore.BLUE}{stage_name.upper():10}{Style.RESET_ALL} | {color}{status:7}{Style.RESET_ALL} | {instr}")
        
        print("-" * 80)
        
        # Print statistics
        print(f"Program Counter: {self.pipeline.pc}")
        print(f"Stalls: {self.pipeline.stalls}")
        print(f"Hazards: Data={self.pipeline.hazards['data']}, Control={self.pipeline.hazards['control']}, Structural={self.pipeline.hazards['structural']}")
        print("=" * 80)
        
        # Slow down visualization for readability
        time.sleep(0.5)
    
    def save_timeline(self, filename="pipeline_timeline.html"):
        """Generate an HTML timeline visualization of the pipeline execution"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CPU Pipeline Timeline</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .timeline { display: flex; flex-direction: column; }
                .cycle { display: flex; margin-bottom: 5px; }
                .cycle-num { width: 50px; font-weight: bold; }
                .stage { width: 150px; padding: 5px; margin-right: 2px; border: 1px solid #ccc; }
                .busy { background-color: #ffff99; }
                .stalled { background-color: #ff9999; }
                .idle { background-color: #99ff99; }
                .instruction { font-family: monospace; }
                h1, h2 { color: #333366; }
                .stats { margin-top: 30px; }
            </style>
        </head>
        <body>
            <h1>CPU Pipeline Timeline</h1>
            <div class="timeline">
        """
        
        # Add cycle information
        for state in self.history:
            html_content += f'<div class="cycle">\n'
            html_content += f'<div class="cycle-num">Cycle {state["cycle"]}</div>\n'
            
            for stage_name in ['fetch', 'decode', 'execute', 'memory', 'writeback']:
                stage_state = state[stage_name]
                if stage_state['stall']:
                    status_class = "stalled"
                    status_text = "STALLED"
                elif stage_state['busy']:
                    status_class = "busy"
                    status_text = "BUSY"
                else:
                    status_class = "idle"
                    status_text = "IDLE"
                
                instr = stage_state['instruction'] if stage_state['instruction'] else "NOP"
                html_content += f'<div class="stage {status_class}">{stage_name.upper()}: {status_text}<br/><span class="instruction">{instr}</span></div>\n'
            
            html_content += '</div>\n'
        
        # Add statistics
        html_content += """
            </div>
            <div class="stats">
                <h2>Pipeline Statistics</h2>
        """
        
        html_content += f"<p>Total Cycles: {self.pipeline.cycles}</p>\n"
        html_content += f"<p>Instructions Executed: {len(self.pipeline.program)}</p>\n"
        html_content += f"<p>Stalls: {self.pipeline.stalls}</p>\n"
        
        if len(self.pipeline.program) > 0:
            cpi = self.pipeline.cycles / len(self.pipeline.program)
            html_content += f"<p>CPI (Cycles per Instruction): {cpi:.2f}</p>\n"
        
        html_content += "<p>Hazards:</p>\n<ul>\n"
        for hazard_type, count in self.pipeline.hazards.items():
            html_content += f"<li>{hazard_type}: {count}</li>\n"
        html_content += "</ul>\n"
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Write to file
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"Timeline saved to {filename}")

def visualize_pipeline(program_file=None):
    """Run the pipeline with visualization"""
    from simulator.processor import Processor
    from simulator.instruction_set import InstructionSet
    
    # Initialize components
    instruction_set = InstructionSet()
    processor = Processor()
    pipeline = Pipeline(processor, instruction_set)
    visualizer = PipelineVisualizer(pipeline)
    
    # Override the run method to include visualization
    original_run = pipeline.run
    
    def run_with_visualization(self):
        """Override run method to include visualization"""
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
            
            # Record and visualize the state
            self.visualizer.record_state()
            self.visualizer.print_horizontal_view()
    
    # Monkey patch the run method
    pipeline.run = run_with_visualization.__get__(pipeline)
    
    # Run simulation
    if program_file:
        pipeline.load_program(program_file)
    else:
        pipeline.load_test_program()
    
    pipeline.run()
    pipeline.show_stats()
    
    # Save visualization timeline
    visualizer.save_timeline()

if __name__ == "__main__":
    # Run with command line arguments
    if len(sys.argv) > 1:
        program_file = sys.argv[1]
        visualize_pipeline(program_file)
    else:
        visualize_pipeline()
