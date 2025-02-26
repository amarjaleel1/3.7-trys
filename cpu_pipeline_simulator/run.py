#!/usr/bin/env python3
import os
import sys
import argparse

# Add the project directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the necessary classes directly from their modules
from simulator.pipeline import Pipeline
from simulator.processor import Processor
from simulator.instruction_set import InstructionSet

def run_simulator(args):
    """Run the CPU pipeline simulator"""
    # Initialize components
    instruction_set = InstructionSet()
    processor = Processor()
    pipeline = Pipeline(processor, instruction_set)
    
    # Set verbosity before running
    pipeline.verbose = not args.quiet
    
    # Run simulation
    if args.program:
        pipeline.load_program(args.program)
    else:
        pipeline.load_test_program()
    
    pipeline.run()
    pipeline.show_stats()

def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(description="CPU Pipeline Simulator")
    parser.add_argument("program", nargs="?", help="Program file to simulate")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run in quiet mode (minimal output)")
    
    args = parser.parse_args()
    
    print("CPU Pipeline Simulator")
    print("=====================")
    
    run_simulator(args)

if __name__ == "__main__":
    main()
