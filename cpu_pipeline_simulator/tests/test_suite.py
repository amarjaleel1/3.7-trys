import unittest
import sys
import os
import tempfile

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cpu_pipeline_simulator.simulator.processor import Processor
from cpu_pipeline_simulator.simulator.instruction_set import InstructionSet
from cpu_pipeline_simulator.simulator.pipeline import Pipeline, PipelineStage

class TestPipelineStage(unittest.TestCase):
    def test_init(self):
        """Test PipelineStage initialization"""
        stage = PipelineStage("TestStage")
        self.assertEqual(stage.name, "TestStage")
        self.assertEqual(stage.instruction, None)
        self.assertFalse(stage.busy)
        self.assertFalse(stage.stall)
    
    def test_is_free(self):
        """Test PipelineStage is_free method"""
        stage = PipelineStage("TestStage")
        self.assertTrue(stage.is_free())
        
        stage.busy = True
        self.assertFalse(stage.is_free())
        
        stage.busy = False
        stage.stall = True
        self.assertFalse(stage.is_free())
        
        stage.stall = False
        self.assertTrue(stage.is_free())

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = Processor()
    
    def test_register_operations(self):
        """Test register read/write operations"""
        # Write to register
        self.processor.write_register("R1", 42)
        self.assertEqual(self.processor.read_register("R1"), 42)
        
        # R0 should always be 0
        self.processor.write_register("R0", 42)
        self.assertEqual(self.processor.read_register("R0"), 0)
        
        # Invalid registers
        with self.assertRaises(ValueError):
            self.processor.read_register("R99")
        
        with self.assertRaises(ValueError):
            self.processor.write_register("R99", 42)
    
    def test_memory_operations(self):
        """Test memory operations"""
        # Write to memory
        self.processor.write_memory(100, 42)
        self.assertEqual(self.processor.read_memory(100), 42)
        
        # Uninitialized memory
        self.assertEqual(self.processor.read_memory(999), 0)
    
    def test_alu_operations(self):
        """Test ALU operations"""
        self.assertEqual(self.processor.execute_alu("ADD", 5, 3), 8)
        self.assertEqual(self.processor.execute_alu("SUB", 5, 3), 2)
        self.assertEqual(self.processor.execute_alu("MUL", 5, 3), 15)
        self.assertEqual(self.processor.execute_alu("DIV", 6, 3), 2)
        self.assertEqual(self.processor.execute_alu("DIV", 5, 0), 0)  # Division by zero
        self.assertEqual(self.processor.execute_alu("AND", 5, 3), 1)
        self.assertEqual(self.processor.execute_alu("OR", 5, 3), 7)
        self.assertEqual(self.processor.execute_alu("XOR", 5, 3), 6)
        
        with self.assertRaises(ValueError):
            self.processor.execute_alu("UNKNOWN", 5, 3)

class TestInstructionSet(unittest.TestCase):
    def setUp(self):
        self.instr_set = InstructionSet()
    
    def test_parse_r_type(self):
        """Test parsing R-type instructions"""
        instr = "ADD R1, R2, R3"
        parsed = self.instr_set.parse_instruction(instr)
        self.assertEqual(parsed['op_code'], "ADD")
        self.assertEqual(parsed['type'], "R")
        self.assertEqual(parsed['operands'], ["R1", "R2", "R3"])
    
    def test_parse_i_type_load_store(self):
        """Test parsing I-type load/store instructions"""
        instr = "LW R1, 100(R2)"
        parsed = self.instr_set.parse_instruction(instr)
        self.assertEqual(parsed['op_code'], "LW")
        self.assertEqual(parsed['type'], "I")
        self.assertEqual(parsed['operands'], ["R1", "100", "R2"])
        
        instr = "SW R1, 100(R2)"
        parsed = self.instr_set.parse_instruction(instr)
        self.assertEqual(parsed['op_code'], "SW")
        self.assertEqual(parsed['type'], "I")
        self.assertEqual(parsed['operands'], ["R1", "100", "R2"])
    
    def test_parse_i_type_branch(self):
        """Test parsing I-type branch instructions"""
        instr = "BEQ R1, R2, 100"
        parsed = self.instr_set.parse_instruction(instr)
        self.assertEqual(parsed['op_code'], "BEQ")
        self.assertEqual(parsed['type'], "I")
        self.assertEqual(parsed['operands'], ["R1", "R2", "100"])
    
    def test_parse_j_type(self):
        """Test parsing J-type instructions"""
        instr = "JUMP 100"
        parsed = self.instr_set.parse_instruction(instr)
        self.assertEqual(parsed['op_code'], "JUMP")
        self.assertEqual(parsed['type'], "J")
        self.assertEqual(parsed['operands'], ["100"])
    
    def test_invalid_instruction(self):
        """Test parsing invalid instructions"""
        instr = "FOO R1, R2"
        with self.assertRaises(ValueError):
            self.instr_set.parse_instruction(instr)
    
    def test_get_registers(self):
        """Test extracting registers from instructions"""
        # R-type
        instr = "ADD R1, R2, R3"
        self.assertEqual(self.instr_set.get_destination_register(instr), "R1")
        self.assertEqual(self.instr_set.get_source_registers(instr), ["R2", "R3"])
        
        # I-type load
        instr = "LW R1, 100(R2)"
        self.assertEqual(self.instr_set.get_destination_register(instr), "R1")
        self.assertEqual(self.instr_set.get_source_registers(instr), ["R2"])
        
        # I-type store
        instr = "SW R1, 100(R2)"
        self.assertEqual(self.instr_set.get_destination_register(instr), None)
        self.assertEqual(self.instr_set.get_source_registers(instr), ["R1", "R2"])
        
        # J-type
        instr = "JUMP 100"
        self.assertEqual(self.instr_set.get_destination_register(instr), None)
        self.assertEqual(self.instr_set.get_source_registers(instr), [])
    
    def test_dependency_detection(self):
        """Test dependency detection between instructions"""
        instr1 = "ADD R1, R2, R3"  # R1 = R2 + R3
        instr2 = "SUB R4, R1, R5"  # R4 = R1 - R5
        self.assertTrue(self.instr_set.has_dependency(instr1, instr2))
        
        instr1 = "ADD R1, R2, R3"  # R1 = R2 + R3
        instr2 = "SUB R4, R5, R6"  # R4 = R5 - R6
        self.assertFalse(self.instr_set.has_dependency(instr1, instr2))

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.processor = Processor()
        self.instr_set = InstructionSet()
        self.pipeline = Pipeline(self.processor, self.instr_set)
    
    def test_init(self):
        """Test Pipeline initialization"""
        self.assertEqual(self.pipeline.cycles, 0)
        self.assertEqual(self.pipeline.stalls, 0)
        self.assertEqual(len(self.pipeline.stages), 5)
        self.assertIn('fetch', self.pipeline.stages)
        self.assertIn('decode', self.pipeline.stages)
        self.assertIn('execute', self.pipeline.stages)
        self.assertIn('memory', self.pipeline.stages)
        self.assertIn('writeback', self.pipeline.stages)
    
    def test_load_program(self):
        """Test loading a program from a file"""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"ADD R1, R0, 10\nADD R2, R0, 5\n")
            temp_file.close()
            self.pipeline.load_program(temp_file.name)
            os.remove(temp_file.name)
        
        self.assertEqual(len(self.pipeline.program), 2)
        self.assertEqual(self.pipeline.program[0], "ADD R1, R0, 10")
        self.assertEqual(self.pipeline.program[1], "ADD R2, R0, 5")
    
    def test_load_program_file_not_found(self):
        """Test loading a program from a non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.pipeline.load_program("non_existent_file.txt")
    
    def test_run(self):
        """Test running the pipeline"""
        self.pipeline.load_test_program()
        self.pipeline.run()
        self.assertEqual(self.pipeline.cycles, 5)
        self.assertEqual(self.pipeline.stalls, 0)
        self.assertEqual(self.pipeline.pc, 5)
    
    def test_check_hazards(self):
        """Test hazard detection"""
        self.assertFalse(self.pipeline.check_hazards())

if __name__ == '__main__':
    unittest.main()
