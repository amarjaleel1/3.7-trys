import sys
import os

# Add the project directory to the Python path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import directly from the module
from simulator.pipeline import Pipeline
from simulator.processor import Processor
from simulator.instruction_set import InstructionSet

def main():
    """
    Main entry point for CPU Pipeline Simulator
    """
    print("CPU Pipeline Simulator")
    print("=====================")
    
    try:
        # Initialize components
        instruction_set = InstructionSet()
        processor = Processor()
        pipeline = Pipeline(processor, instruction_set)
        
        # Run simulation
        if len(sys.argv) > 1:
            program_file = sys.argv[1]
            pipeline.load_program(program_file)
        else:
            pipeline.load_test_program()
        
        pipeline.run()
        pipeline.show_stats()
    except ImportError as e:
        print(f"Import Error: {e}")
        print("\nCheck that all modules are correctly structured and exported.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
