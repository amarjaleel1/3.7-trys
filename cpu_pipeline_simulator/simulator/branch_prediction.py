"""
Branch Prediction implementation for the CPU Pipeline Simulator.
Includes multiple branch prediction strategies.
"""

class BranchPredictor:
    """Base class for branch predictors"""
    def __init__(self):
        self.predictions = 0
        self.correct_predictions = 0
    
    def predict(self, pc, instruction):
        """Predict whether a branch will be taken"""
        raise NotImplementedError("Subclasses must implement predict()")
    
    def update(self, pc, instruction, taken):
        """Update prediction history based on actual outcome"""
        raise NotImplementedError("Subclasses must implement update()")
    
    def accuracy(self):
        """Return prediction accuracy"""
        if self.predictions == 0:
            return 0.0
        return self.correct_predictions / self.predictions
    
    def stats(self):
        """Return statistics about prediction accuracy"""
        return {
            'predictions': self.predictions,
            'correct': self.correct_predictions,
            'accuracy': self.accuracy()
        }


class AlwaysTakenPredictor(BranchPredictor):
    """Simple predictor that always predicts branch taken"""
    
    def predict(self, pc, instruction):
        """Predict branch taken"""
        return True
    
    def update(self, pc, instruction, taken):
        """Update prediction stats"""
        self.predictions += 1
        if taken:
            self.correct_predictions += 1


class AlwaysNotTakenPredictor(BranchPredictor):
    """Simple predictor that always predicts branch not taken"""
    
    def predict(self, pc, instruction):
        """Predict branch not taken"""
        return False
    
    def update(self, pc, instruction, taken):
        """Update prediction stats"""
        self.predictions += 1
        if not taken:
            self.correct_predictions += 1


class TwoBitPredictor(BranchPredictor):
    """
    Two-bit saturating counter branch predictor
    
    States:
    0 - Strongly Not Taken
    1 - Weakly Not Taken
    2 - Weakly Taken
    3 - Strongly Taken
    """
    
    def __init__(self):
        super().__init__()
        self.branch_history = {}  # PC -> state mapping
    
    def predict(self, pc, instruction):
        """Predict branch based on 2-bit state"""
        state = self.branch_history.get(pc, 1)  # Default to Weakly Not Taken
        return state >= 2  # Taken if state is 2 or 3
    
    def update(self, pc, instruction, taken):
        """Update branch history based on outcome"""
        self.predictions += 1
        
        state = self.branch_history.get(pc, 1)  # Default to Weakly Not Taken
        
        # Update state based on outcome
        if taken:
            if state < 3:
                state += 1
            if state >= 2:
                self.correct_predictions += 1
        else:
            if state > 0:
                state -= 1
            if state < 2:
                self.correct_predictions += 1
        
        self.branch_history[pc] = state


class CorrelatingPredictor(BranchPredictor):
    """
    Correlating branch predictor that uses global history
    to make predictions (2-bit counters with N-bit global history)
    """
    
    def __init__(self, history_bits=2):
        super().__init__()
        self.history_bits = history_bits
        self.global_history = 0
        self.history_mask = (1 << history_bits) - 1
        self.pattern_table = {}  # (PC, global_history) -> state mapping
    
    def predict(self, pc, instruction):
        """Predict branch based on global history pattern"""
        pattern = (pc, self.global_history)
        state = self.pattern_table.get(pattern, 1)  # Default to Weakly Not Taken
        return state >= 2  # Taken if state is 2 or 3
    
    def update(self, pc, instruction, taken):
        """Update branch history based on outcome"""
        self.predictions += 1
        
        pattern = (pc, self.global_history)
        state = self.pattern_table.get(pattern, 1)  # Default to Weakly Not Taken
        
        # Update state based on outcome
        if taken:
            if state < 3:
                state += 1
            if state >= 2:
                self.correct_predictions += 1
        else:
            if state > 0:
                state -= 1
            if state < 2:
                self.correct_predictions += 1
        
        self.pattern_table[pattern] = state
        
        # Update global history
        self.global_history = ((self.global_history << 1) | int(taken)) & self.history_mask


# Factory function to create branch predictors
def create_branch_predictor(strategy='two_bit'):
    """Create a branch predictor based on the specified strategy"""
    predictors = {
        'always_taken': AlwaysTakenPredictor,
        'always_not_taken': AlwaysNotTakenPredictor,
        'two_bit': TwoBitPredictor,
        'correlating': CorrelatingPredictor
    }
    
    if strategy not in predictors:
        raise ValueError(f"Unknown branch prediction strategy: {strategy}")
    
    return predictors[strategy]()
