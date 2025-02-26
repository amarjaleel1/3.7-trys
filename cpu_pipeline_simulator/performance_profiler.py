import os
import sys
import time
import json
import argparse
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# Add the project directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from simulator.pipeline import Pipeline
from simulator.processor import Processor
from simulator.instruction_set import InstructionSet

class PipelineProfiler:
    """
    Performance profiling tool for the CPU Pipeline Simulator
    """
    
    def __init__(self, pipeline):
        """Initialize with a pipeline instance"""
        self.pipeline = pipeline
        self.cycles_per_instruction = []
        self.instruction_frequencies = defaultdict(int)
        self.stalls_per_cycle = []
        self.hazards_per_cycle = {
            'data': [],
            'control': [],
            'structural': []
        }
        self.pipeline_states = []
        
        # Add hooks to the pipeline
        self._add_profiling_hooks()
    
    def _add_profiling_hooks(self):
        """Add profiling hooks to the pipeline"""
        # Save original methods that we're going to override
        self.original_run = self.pipeline.run
        
        # Override the run method to collect data
        def profiled_run(self_):
            """Profiled version of the pipeline run method"""
            start_time = time.time()
            
            while self_.pc < len(self_.program) or any(stage.instruction for stage in self_.stages.values()):
                self_.cycles += 1
                
                # Execute stages in reverse order to avoid overwriting
                self_._execute_writeback()
                self_._execute_memory()
                self_._execute_execute()
                self_._execute_decode()
                self_._execute_fetch()
                
                # Check for hazards
                if self_.check_hazards():
                    self_.stalls += 1
                
                # Record data for profiling
                self._record_cycle_data()
            
            end_time = time.time()
            self.execution_time = end_time - start_time
        
        # Apply the override
        self.pipeline.run = profiled_run.__get__(self.pipeline)
    
    def _record_cycle_data(self):
        """Record data for the current cycle"""
        # Record CPI data
        if len(self.pipeline.program) > 0:
            self.cycles_per_instruction.append(self.pipeline.cycles / len(self.pipeline.program))
        
        # Record instruction frequency
        for stage_name, stage in self.pipeline.stages.items():
            if stage.instruction:
                op_code = stage.instruction.split()[0]
                self.instruction_frequencies[op_code] += 1
        
        # Record stalls
        self.stalls_per_cycle.append(self.pipeline.stalls)
        
        # Record hazards
        for hazard_type in self.hazards_per_cycle:
            self.hazards_per_cycle[hazard_type].append(self.pipeline.hazards[hazard_type])
        
        # Record pipeline state
        state = {}
        for stage_name, stage in self.pipeline.stages.items():
            state[stage_name] = {
                'instruction': stage.instruction,
                'busy': stage.busy,
                'stall': stage.stall
            }
        self.pipeline_states.append(state)
    
    def reset(self):
        """Reset the profiler data"""
        self.cycles_per_instruction = []
        self.instruction_frequencies = defaultdict(int)
        self.stalls_per_cycle = []
        for hazard_type in self.hazards_per_cycle:
            self.hazards_per_cycle[hazard_type] = []
        self.pipeline_states = []
    
    def generate_report(self, format='text'):
        """Generate a performance report"""
        if format == 'text':
            return self._generate_text_report()
        elif format == 'html':
            return self._generate_html_report()
        elif format == 'json':
            return self._generate_json_report()
        else:
            raise ValueError(f"Unknown report format: {format}")
    
    def _generate_text_report(self):
        """Generate a text performance report"""
        report = []
        report.append("CPU Pipeline Simulator - Performance Report")
        report.append("==========================================")
        report.append("")
        
        # Basic statistics
        report.append("Basic Statistics:")
        report.append(f"Total Cycles: {self.pipeline.cycles}")
        report.append(f"Instructions Executed: {len(self.pipeline.program)}")
        report.append(f"Stalls: {self.pipeline.stalls}")
        if len(self.pipeline.program) > 0:
            report.append(f"CPI (Cycles per Instruction): {self.pipeline.cycles / len(self.pipeline.program):.2f}")
        report.append(f"Execution Time: {self.execution_time:.4f} seconds")
        report.append("")
        
        # Hazard statistics
        report.append("Hazard Statistics:")
        for hazard_type, count in self.pipeline.hazards.items():
            report.append(f"  {hazard_type}: {count}")
        report.append("")
        
        # Instruction frequencies
        report.append("Instruction Frequencies:")
        for op_code, count in sorted(self.instruction_frequencies.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {op_code}: {count}")
        report.append("")
        
        return "\n".join(report)
    
    def _generate_html_report(self):
        """Generate an HTML performance report with charts"""
        # Create the charts
        self._create_charts("report_charts")
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CPU Pipeline Simulator - Performance Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #2c3e50; }
                .stats-container { display: flex; flex-wrap: wrap; }
                .stat-box { 
                    width: 200px; 
                    height: 100px; 
                    margin: 10px; 
                    padding: 10px; 
                    border-radius: 5px;
                    color: white;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                .stat-box h3 { margin: 0; }
                .stat-box p { margin: 5px 0; font-size: 24px; font-weight: bold; }
                .blue { background-color: #3498db; }
                .green { background-color: #2ecc71; }
                .orange { background-color: #e67e22; }
                .red { background-color: #e74c3c; }
                .chart { margin: 20px 0; }
                pre { background-color: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>CPU Pipeline Simulator - Performance Report</h1>
            
            <h2>Key Performance Indicators</h2>
            <div class="stats-container">
                <div class="stat-box blue">
                    <h3>Total Cycles</h3>
                    <p>{cycles}</p>
                </div>
                <div class="stat-box green">
                    <h3>Instructions</h3>
                    <p>{instructions}</p>
                </div>
                <div class="stat-box orange">
                    <h3>Stalls</h3>
                    <p>{stalls}</p>
                </div>
                <div class="stat-box red">
                    <h3>CPI</h3>
                    <p>{cpi:.2f}</p>
                </div>
            </div>
            
            <h2>Execution Time</h2>
            <p>{execution_time:.4f} seconds</p>
            
            <h2>Charts</h2>
            
            <div class="chart">
                <h3>CPI over Time</h3>
                <img src="report_charts/cpi_over_time.png" alt="CPI over Time" width="800">
            </div>
            
            <div class="chart">
                <h3>Instruction Frequency</h3>
                <img src="report_charts/instruction_frequency.png" alt="Instruction Frequency" width="800">
            </div>
            
            <div class="chart">
                <h3>Hazards over Time</h3>
                <img src="report_charts/hazards_over_time.png" alt="Hazards over Time" width="800">
            </div>
            
            <h2>Raw Performance Data</h2>
            <pre>{raw_data}</pre>
            
            <footer>
                <p>Report generated on {date}</p>
            </footer>
        </body>
        </html>
        """.format(
            cycles=self.pipeline.cycles,
            instructions=len(self.pipeline.program),
            stalls=self.pipeline.stalls,
            cpi=self.pipeline.cycles / len(self.pipeline.program) if len(self.pipeline.program) > 0 else 0,
            execution_time=self.execution_time,
            raw_data=self._generate_text_report(),
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return html
    
    def _generate_json_report(self):
        """Generate a JSON performance report"""
        data = {
            "basic_statistics": {
                "total_cycles": self.pipeline.cycles,
                "instructions_executed": len(self.pipeline.program),
                "stalls": self.pipeline.stalls,
                "cpi": self.pipeline.cycles / len(self.pipeline.program) if len(self.pipeline.program) > 0 else 0,
                "execution_time": self.execution_time
            },
            "hazards": self.pipeline.hazards,
            "instruction_frequencies": self.instruction_frequencies,
            "cycles_per_instruction": self.cycles_per_instruction,
            "stalls_per_cycle": self.stalls_per_cycle,
            "hazards_per_cycle": self.hazards_per_cycle,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(data, indent=2)
    
    def _create_charts(self, output_dir):
        """Create performance charts"""
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # CPI over time
        plt.figure(figsize=(10, 6))
        plt.plot(self.cycles_per_instruction)
        plt.title('CPI over Time')
        plt.xlabel('Cycle')
        plt.ylabel('Cycles per Instruction')
        plt.grid(True)
        plt.savefig(f"{output_dir}/cpi_over_time.png")
        
        # Instruction frequency
        plt.figure(figsize=(10, 6))
        instructions = list(self.instruction_frequencies.keys())
        counts = list(self.instruction_frequencies.values())
        plt.bar(instructions, counts)
        plt.title('Instruction Frequency')
        plt.xlabel('Instruction')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/instruction_frequency.png")
        
        # Hazards over time
        plt.figure(figsize=(10, 6))
        for hazard_type, counts in self.hazards_per_cycle.items():
            plt.plot(counts, label=hazard_type)
        plt.title('Hazards over Time')
        plt.xlabel('Cycle')
        plt.ylabel('Count')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{output_dir}/hazards_over_time.png")

def profile_pipeline(program_file=None, report_format='text', report_output=None):
    """Run pipeline with profiling"""
    # Initialize components
    instruction_set = InstructionSet()
    processor = Processor()
    pipeline = Pipeline(processor, instruction_set)
    profiler = PipelineProfiler(pipeline)
    
    # Run simulation
    if program_file:
        pipeline.load_program(program_file)
    else:
        pipeline.load_test_program()
    
    pipeline.run()
    pipeline.show_stats()
    
    # Generate report
    report