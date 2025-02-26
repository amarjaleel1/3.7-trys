# Project Structure

This document outlines the structure of the CPU Pipeline Simulator project.

```
cpu_pipeline_simulator/
├── __init__.py                  # Package initialization
├── main.py                     # Main entry point
├── run.py                      # Enhanced runner with argument parsing
├── setup.py                    # Package setup information
├── LICENSE                     # License file
├── README.md                   # Project documentation
├── STRUCTURE.md                # This file
├── .gitignore                  # Git ignore file
├── simulator/                  # Main simulator package
│   ├── __init__.py             # Package initialization
│   ├── pipeline.py             # Pipeline implementation
│   ├── processor.py            # Processor and ALU implementation
│   └── instruction_set.py      # Instruction set definitions
├── tests/                      # Test suite
│   ├── __init__.py             # Test package initialization
│   └── test_processor.py       # Processor unit tests
└── sample_programs/            # Example programs
    └── simple_program.txt      # Simple test program
```

## Module Dependencies

- `main.py` depends on `simulator.pipeline`, `simulator.processor`, and `simulator.instruction_set`
- `simulator.pipeline` depends on `simulator.processor` and `simulator.instruction_set`
- `simulator.processor` has no internal dependencies
- `simulator.instruction_set` has no internal dependencies

## Class Relationships

- `Pipeline` uses `Processor` and `InstructionSet`
- `Pipeline` contains multiple `PipelineStage` instances
- `InstructionSet` provides instruction parsing and dependency detection
- `Processor` handles register file, memory, and ALU operations
