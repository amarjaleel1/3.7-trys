# CPU Pipeline Simulator

A simulation of a 5-stage RISC CPU pipeline with hazard detection and mitigation.

## Features

- 5-stage pipeline (Fetch, Decode, Execute, Memory, Writeback)
- Data hazard detection and stalling
- Control hazard handling
- Detailed cycle-by-cycle pipeline visualization
- Performance statistics

## Usage

```bash
python main.py [program_file]
```

For more options:
```bash
python run.py --help
```

If no program file is specified, a default test program will be loaded.

## Instruction Set

The simulator supports the following instruction types:

### R-Type Instructions
- ADD Rd, Rs, Rt  (Rd = Rs + Rt)
- SUB Rd, Rs, Rt  (Rd = Rs - Rt)
- MUL Rd, Rs, Rt  (Rd = Rs * Rt)
- DIV Rd, Rs, Rt  (Rd = Rs / Rt)
- AND Rd, Rs, Rt  (Rd = Rs & Rt)
- OR Rd, Rs, Rt   (Rd = Rs | Rt)
- XOR Rd, Rs, Rt  (Rd = Rs ^ Rt)

### I-Type Instructions
- LW Rt, offset(Rs)  (Rt = Memory[Rs + offset])
- SW Rt, offset(Rs)  (Memory[Rs + offset] = Rt)
- BEQ Rs, Rt, offset (if Rs == Rt, PC = PC + offset)
- BNE Rs, Rt, offset (if Rs != Rt, PC = PC + offset)

### J-Type Instructions
- JUMP target  (PC = target)
- JAL target   (R31 = PC + 4, PC = target)

## Program Format

Each instruction should be on its own line. Comments start with '#' character.

Example:
```
# Initialize values
ADD R1, R0, 10    # R1 = 10
ADD R2, R0, 5     # R2 = 5

# Calculate result
MUL R3, R1, R2    # R3 = R1 * R2 = 50
```

## Pipeline Stages

1. **Fetch**: Read instruction from memory
2. **Decode**: Decode instruction and read registers
3. **Execute**: Perform ALU operations
4. **Memory**: Access memory (if needed)
5. **Writeback**: Write results back to registers

## Hazards

The simulator detects and handles:
- Data hazards (RAW, WAR, WAW)
- Control hazards (branches and jumps)
- Structural hazards (resource conflicts)

## Running Tests

To run the test suite:

```bash
python -m unittest discover tests
```

## Future Improvements

- Forwarding to reduce stalls
- Branch prediction
- Out-of-order execution
- Support for more complex instructions

## Suggestions for New Features

- Implement a graphical user interface (GUI) for better visualization and interaction.
- Add support for more complex instruction sets, including floating-point operations.
- Implement a more advanced branch prediction algorithm.
- Add support for multi-core simulation.
- Include a cache memory simulation to study the effects of cache on performance.
- Implement a more detailed memory hierarchy, including L1, L2, and L3 caches.
- Add support for different pipeline configurations, such as superscalar and VLIW architectures.
- Implement a more detailed power consumption model to study the effects of different pipeline configurations on power usage.
- Add support for different types of hazards, such as structural hazards and control hazards.
- Implement a more detailed performance analysis tool, including support for different types of performance metrics.

## Advanced Branch Prediction Strategies

The simulator now includes advanced branch prediction strategies such as:
- Global history-based predictors
- Tournament predictors
- Machine learning-based predictors

These strategies help improve the accuracy and efficiency of branch prediction, leading to better overall performance.

## Out-of-Order Execution

The simulator now supports out-of-order execution, which allows instructions to be executed as soon as their operands are ready, rather than strictly in program order. This feature includes:
- Reservation stations
- Reorder buffers
- Register renaming

Out-of-order execution helps improve the utilization of functional units and reduces the impact of instruction dependencies on performance.

## Git Repository

You can find the source code for this project on GitHub:
https://github.com/yourusername/cpu-pipeline-simulator

## How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
