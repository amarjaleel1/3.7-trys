"""
Diagnostic tool to check if imports work correctly
"""
import sys
import os
import importlib

def check_import(module_name):
    try:
        module = importlib.import_module(module_name)
        print(f"✅ Successfully imported {module_name}")
        return module
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return None

def check_class_in_module(module, class_name):
    if module is None:
        return
    
    if hasattr(module, class_name):
        print(f"✅ Successfully found class {class_name} in {module.__name__}")
    else:
        print(f"❌ Class {class_name} not found in {module.__name__}")
        if hasattr(module, "__all__"):
            print(f"   Module exports: {module.__all__}")
        else:
            print(f"   Module has no __all__ defined")

def main():
    print("Checking import structure for CPU Pipeline Simulator")
    print("=================================================\n")
    
    # Add the project directory to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    print(f"Python path includes: {current_dir}\n")
    
    # Check simulator package
    simulator = check_import("simulator")
    
    # Check module imports
    pipeline_module = check_import("simulator.pipeline")
    processor_module = check_import("simulator.processor")
    instruction_set_module = check_import("simulator.instruction_set")
    
    # Check class imports
    check_class_in_module(pipeline_module, "Pipeline")
    check_class_in_module(pipeline_module, "PipelineStage")
    check_class_in_module(processor_module, "Processor")
    check_class_in_module(instruction_set_module, "InstructionSet")
    
    print("\nDiagnostic complete.")

if __name__ == "__main__":
    main()
