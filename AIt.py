import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class AITutorial:
    def __init__(self):
        self.lessons = {
            1: self.intro_to_python,
            2: self.variables_and_data_types,
            3: self.control_structures,
            4: self.functions,
            5: self.intro_to_ai,
            6: self.linear_regression_demo,
            7: self.simple_neural_network
        }
        
    def start(self):
        """Main method to start the tutorial"""
        print("\n" + "="*50)
        print("🤖 WELCOME TO AI AND PYTHON BASICS TUTORIAL 🐍")
        print("="*50 + "\n")
        
        print("This interactive tutorial will teach you the basics of Python programming")
        print("and introduce fundamental AI concepts with visualizations.\n")
        
        while True:
            self.display_menu()
            try:
                choice = int(input("\nEnter the lesson number (0 to exit): "))
                if choice == 0:
                    print("\nThank you for learning with us! Happy coding! 👋\n")
                    break
                elif choice in self.lessons:
                    self.lessons[choice]()
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid choice. Please select a valid lesson number.")
            except ValueError:
                print("Please enter a number.")
    
    def display_menu(self):
        """Display the tutorial menu"""
        print("\n📚 AVAILABLE LESSONS:")
        print("------------------------")
        print("1. Introduction to Python")
        print("2. Variables and Data Types")
        print("3. Control Structures")
        print("4. Functions in Python")
        print("5. Introduction to AI Concepts")
        print("6. Linear Regression Demo")
        print("7. Simple Neural Network Visualization")
        print("0. Exit Tutorial")
    
    def intro_to_python(self):
        """Lesson 1: Introduction to Python"""
        print("\n" + "="*50)
        print("LESSON 1: INTRODUCTION TO PYTHON")
        print("="*50 + "\n")
        
        print("Python is a high-level, interpreted programming language known for its")
        print("readability and simplicity. It's widely used in AI, data science, web development,")
        print("automation, and many other fields.\n")
        
        print("Let's start with a simple 'Hello, World!' program:")
        time.sleep(1)
        
        code = 'print("Hello, World!")'
        print(f"\n```python\n{code}\n```")
        
        print("\nOutput:")
        print("Hello, World!")
        
        print("\nPython features that make it perfect for AI:")
        features = [
            "Simple and readable syntax",
            "Rich ecosystem of libraries (NumPy, Pandas, TensorFlow, PyTorch)",
            "Great for prototyping and production",
            "Strong community support"
        ]
        
        for i, feature in enumerate(features, 1):
            time.sleep(0.5)
            print(f"{i}. {feature}")
            
        self.visualize_python_popularity()
    
    def visualize_python_popularity(self):
        """Visualize Python's popularity growth"""
        print("\nLet's visualize Python's growing popularity in recent years:")
        
        years = np.array([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
        popularity = np.array([10, 12, 15, 19, 22, 27, 31, 35, 38, 40, 43])
        
        plt.figure(figsize=(10, 5))
        plt.plot(years, popularity, 'b-o', linewidth=2, markersize=8)
        plt.title("Python's Growing Popularity")
        plt.xlabel("Year")
        plt.ylabel("Popularity Index")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show(block=False)  # Use block=False to prevent blocking execution
        plt.pause(3)  # Pause to allow viewing
        plt.close()  # Close the plot when done
    
    def variables_and_data_types(self):
        """Lesson 2: Variables and Data Types"""
        print("\n" + "="*50)
        print("LESSON 2: VARIABLES AND DATA TYPES")
        print("="*50 + "\n")
        
        print("Variables are containers for storing data values.")
        print("Python has several standard data types:\n")
        
        data_types = {
            "int": "Integer numbers (1, 2, 3)",
            "float": "Floating point numbers (1.5, 2.75)",
            "str": "Strings - text ('hello', \"world\")",
            "bool": "Boolean values (True, False)",
            "list": "Ordered, changeable collection [1, 2, 3]",
            "tuple": "Ordered, unchangeable collection (1, 2, 3)",
            "dict": "Key-value pairs {'name': 'John', 'age': 30}",
            "set": "Unordered collection of unique items {1, 2, 3}"
        }
        
        for dtype, description in data_types.items():
            time.sleep(0.5)
            print(f"• {dtype}: {description}")
        
        print("\nExample of variable assignments:")
        code = """
# Integer
age = 25

# Float
height = 5.9

# String
name = "Alice"

# Boolean
is_student = True

# List
hobbies = ["reading", "coding", "hiking"]

# Dictionary
person = {
    "name": "Bob",
    "age": 30,
    "is_student": False
}

# Accessing values
print(name)             # Output: Alice
print(hobbies[1])       # Output: coding
print(person["name"])   # Output: Bob
        """
        print(f"\n```python{code}\n```")
        
        self.animate_data_types()
    
    def animate_data_types(self):
        """Animate different data types"""
        print("\nLet's visualize common Python data types:")
        
        data_types = ['int', 'float', 'str', 'bool', 'list', 'dict', 'tuple', 'set']
        popularity = [25, 20, 23, 8, 15, 12, 10, 7]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(data_types, popularity, color='skyblue')
        plt.title('Python Data Types Usage')
        plt.xlabel('Data Type')
        plt.ylabel('Usage Percentage')
        plt.ylim(0, 30)
        
        # Add percentage labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    
    def control_structures(self):
        """Lesson 3: Control Structures"""
        print("\n" + "="*50)
        print("LESSON 3: CONTROL STRUCTURES")
        print("="*50 + "\n")
        
        print("Control structures allow you to control the flow of your program.")
        print("Let's look at the main ones:\n")
        
        # Conditional statements
        print("1. CONDITIONAL STATEMENTS (if, elif, else):")
        code1 = """
x = 10

if x > 15:
    print("x is greater than 15")
elif x > 5:
    print("x is greater than 5 but not greater than 15")
else:
    print("x is 5 or less")
        """
        print(f"\n```python{code1}\n```")
        print("Output: x is greater than 5 but not greater than 15")
        
        # Loops
        print("\n2. LOOPS (for, while):")
        code2 = """
# For loop
print("For loop:")
for i in range(5):
    print(i, end=" ")  # Output: 0 1 2 3 4

# While loop
print("\\nWhile loop:")
count = 0
while count < 5:
    print(count, end=" ")  # Output: 0 1 2 3 4
    count += 1
        """
        print(f"\n```python{code2}\n```")
        
        self.visualize_control_flow()
    
    def visualize_control_flow(self):
        """Visualize control flow with animation"""
        print("\nLet's visualize how a loop works:")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Create a simple static visualization instead of animation
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title("Loop Iterations")
        ax.set_xlabel("Step")
        ax.set_ylabel("Value")
        
        x = list(range(5))
        y = [i**2 for i in x]
        
        ax.plot(x, y, 'bo-', linewidth=2)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        for i, (xi, yi) in enumerate(zip(x, y)):
            ax.text(xi, yi+0.3, f"({xi}, {yi})", ha='center')
        
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    
    def functions(self):
        """Lesson 4: Functions in Python"""
        print("\n" + "="*50)
        print("LESSON 4: FUNCTIONS IN PYTHON")
        print("="*50 + "\n")
        
        print("Functions are reusable blocks of code that perform specific tasks.")
        print("They help in organizing code and promoting reusability.\n")
        
        print("Basic function structure:")
        code1 = """
def function_name(parameters):
    \"\"\"Docstring describing the function\"\"\"
    # Function body - code that runs when called
    return result  # Optional return value
        """
        print(f"\n```python{code1}\n```")
        
        print("\nExample functions:")
        code2 = """
# Simple function that greets a person
def greet(name):
    return f"Hello, {name}!"

# Function with default parameter
def power(base, exponent=2):
    return base ** exponent

# Function with multiple return values
def calculate_statistics(numbers):
    return min(numbers), max(numbers), sum(numbers)/len(numbers)

# Function calls
print(greet("Alice"))  # Output: Hello, Alice!
print(power(3))        # Output: 9 (3^2)
print(power(2, 3))     # Output: 8 (2^3)

min_val, max_val, avg = calculate_statistics([1, 2, 3, 4, 5])
print(f"Min: {min_val}, Max: {max_val}, Average: {avg}")
# Output: Min: 1, Max: 5, Average: 3.0
        """
        print(f"\n```python{code2}\n```")
        
        self.visualize_function()
    
    def visualize_function(self):
        """Visualize functions with different parameters"""
        print("\nLet's visualize a function with different parameters:")
        
        def quadratic(x, a=1, b=0, c=0):
            return a*x**2 + b*x + c
        
        x = np.linspace(-5, 5, 100)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot different parameter combinations
        y1 = quadratic(x)
        y2 = quadratic(x, a=2)
        y3 = quadratic(x, b=2)
        y4 = quadratic(x, c=2)
        
        ax.plot(x, y1, label='f(x) = x²')
        ax.plot(x, y2, label='f(x) = 2x²')
        ax.plot(x, y3, label='f(x) = x² + 2x')
        ax.plot(x, y4, label='f(x) = x² + 2')
        
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        ax.set_title('Quadratic Function with Different Parameters')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    
    def intro_to_ai(self):
        """Lesson 5: Introduction to AI Concepts"""
        print("\n" + "="*50)
        print("LESSON 5: INTRODUCTION TO AI CONCEPTS")
        print("="*50 + "\n")
        
        print("Artificial Intelligence (AI) is a field of computer science focused on creating")
        print("systems that can perform tasks that typically require human intelligence.\n")
        
        print("Key AI concepts:")
        
        concepts = [
            ("Machine Learning", "Algorithms that improve automatically through experience"),
            ("Deep Learning", "Subset of ML using neural networks with multiple layers"),
            ("Neural Networks", "Computing systems inspired by the human brain"),
            ("Supervised Learning", "Learning from labeled training data"),
            ("Unsupervised Learning", "Finding patterns in unlabeled data"),
            ("Reinforcement Learning", "Learning through trial and error with rewards/penalties")
        ]
        
        for concept, description in concepts:
            time.sleep(0.5)
            print(f"• {concept}: {description}")
        
        print("\nAI applications:")
        applications = [
            "Computer Vision (image recognition)",
            "Natural Language Processing (language understanding)",
            "Robotics (autonomous systems)",
            "Recommendation Systems (personalized suggestions)",
            "Predictive Analytics (forecasting future trends)"
        ]
        
        for i, app in enumerate(applications, 1):
            time.sleep(0.5)
            print(f"{i}. {app}")
        
        self.visualize_ai_concepts()
    
    def visualize_ai_concepts(self):
        """Visualize the relationship between AI concepts"""
        print("\nVisualizing the relationship between AI concepts:")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create a hierarchical structure
        ax.axis('off')
        
        def draw_box(x, y, width, height, title, content=None, color='skyblue'):
            rect = plt.Rectangle((x, y), width, height, fill=True, color=color, alpha=0.3, linewidth=2, edgecolor='navy')
            ax.add_patch(rect)
            ax.text(x + width/2, y + height - 0.2, title, ha='center', va='center', fontsize=12, fontweight='bold')
            
            if content:
                for i, line in enumerate(content):
                    ax.text(x + width/2, y + height - 0.5 - i*0.3, line, ha='center', va='center', fontsize=10)
        
        # Main AI box
        draw_box(1, 1, 8, 7, "Artificial Intelligence", ["Systems that can perform tasks", "requiring human intelligence"], color='lightgray')
        
        # ML box
        draw_box(2, 2, 6, 5, "Machine Learning", ["Algorithms that improve", "through experience"])
        
        # Types of ML
        draw_box(2.5, 3, 1.6, 3, "Supervised\nLearning", ["Learning from", "labeled data"])
        draw_box(4.4, 3, 1.6, 3, "Unsupervised\nLearning", ["Finding patterns in", "unlabeled data"])
        draw_box(6.3, 3, 1.6, 3, "Reinforcement\nLearning", ["Learning through", "trial and error"])
        
        # Deep Learning
        draw_box(3.5, 4.5, 3, 1.2, "Deep Learning", ["Using multi-layer", "neural networks"], color='lightgreen')
        
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    
    def linear_regression_demo(self):
        """Lesson 6: Linear Regression Demo"""
        print("\n" + "="*50)
        print("LESSON 6: LINEAR REGRESSION DEMO")
        print("="*50 + "\n")
        
        print("Linear regression is one of the simplest machine learning algorithms.")
        print("It attempts to find a linear relationship between variables.")
        print("Formula: y = mx + b (where m is slope and b is y-intercept)\n")
        
        print("Example Python code for linear regression:")
        code = """
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Sample data (hours studied vs. exam scores)
hours = np.array([[2], [3], [5], [7], [8], [10]])
scores = np.array([65, 70, 80, 85, 90, 95])

# Create and train the model
model = LinearRegression()
model.fit(hours, scores)

# Get model parameters
slope = model.coef_[0]
intercept = model.intercept_

# Make predictions
hours_new = np.array([[1], [4], [6], [9]])
predicted_scores = model.predict(hours_new)

# Display results
print(f"Model equation: score = {slope:.2f} × hours + {intercept:.2f}")
print("Predictions:")
for hour, score in zip(hours_new, predicted_scores):
    print(f"  {hour[0]} hours → {score:.2f} score")
        """
        print(f"\n```python{code}\n```")
        
        self.animate_linear_regression()
    
    def animate_linear_regression(self):
        """Animate how linear regression works"""
        print("\nLet's visualize how linear regression works:")
        
        # Create sample data
        np.random.seed(42)
        x = np.array([2, 3, 5, 7, 8, 10])
        y = 60 + 3.5 * x + np.random.normal(0, 3, size=len(x))
        
        plt.figure(figsize=(10, 6))
        
        # Plot data points
        plt.scatter(x, y, color='blue', s=50, label='Data points')
        plt.xlabel('Hours Studied')
        plt.ylabel('Exam Score')
        plt.title('Linear Regression: Hours Studied vs. Exam Score')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Just show the final fit instead of animation
        m = 3.5  # Target slope
        b = 60   # Target intercept
        
        x_line = np.array([0, 12])
        y_line = b + m * x_line
        plt.plot(x_line, y_line, 'r-', label=f'Final fit: y = {m:.2f}x + {b:.2f}')
        plt.legend()
        
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    
    def simple_neural_network(self):
        """Lesson 7: Simple Neural Network Visualization"""
        print("\n" + "="*50)
        print("LESSON 7: SIMPLE NEURAL NETWORK VISUALIZATION")
        print("="*50 + "\n")
        
        print("Neural networks are a fundamental concept in deep learning,")
        print("inspired by the structure of the human brain.")
        print("They consist of layers of neurons (nodes) that process information.\n")
        
        print("Basic components of a neural network:")
        components = [
            "Input Layer: Receives the initial data",
            "Hidden Layers: Process the data through weighted connections",
            "Output Layer: Produces the final result",
            "Activation Functions: Add non-linearity (e.g., ReLU, Sigmoid, Tanh)",
            "Weights & Biases: Parameters adjusted during training"
        ]
        
        for component in components:
            time.sleep(0.5)
            print(f"• {component}")
        
        print("\nExample code for a simple neural network using TensorFlow/Keras:")
        code = """
import tensorflow as tf
from tensorflow import keras

# Create a simple neural network model
model = keras.Sequential([
    # Input layer (flatten the 28x28 pixel images to a 1D array)
    keras.layers.Flatten(input_shape=(28, 28)),
    
    # Hidden layer with 128 neurons and ReLU activation
    keras.layers.Dense(128, activation='relu'),
    
    # Output layer with 10 neurons (for 10 classes) and softmax activation
    keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Model training would happen here
# model.fit(train_images, train_labels, epochs=5)
        """
        print(f"\n```python{code}\n```")
        
        self.visualize_neural_network()
    
    def visualize_neural_network(self):
        """Visualize a simple neural network"""
        print("\nVisualizing a simple neural network structure:")
        
        plt.figure(figsize=(12, 8))
        
        def draw_neural_network():
            # Set up the axes
            ax = plt.gca()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Layer node positions
            layer_positions = {
                'input': 2,
                'hidden1': 4.5,
                'hidden2': 7,
                'output': 9
            }
            
            # Number of nodes in each layer
            nodes = {
                'input': 4,
                'hidden1': 5,
                'hidden2': 5,
                'output': 3
            }
            
            # Layer names
            layer_names = {
                'input': 'Input Layer',
                'hidden1': 'Hidden Layer 1',
                'hidden2': 'Hidden Layer 2',
                'output': 'Output Layer'
            }
            
            # Node positions for each layer
            node_positions = {}
            
            # Draw each layer
            for layer, x_pos in layer_positions.items():
                # Calculate y-positions for nodes in this layer
                n_nodes = nodes[layer]
                spacing = 8 / (n_nodes + 1)
                
                node_positions[layer] = []
                
                # Add layer name
                plt.text(x_pos, 9.5, layer_names[layer], ha='center', va='center', 
                         fontsize=14, fontweight='bold')
                
                # Draw nodes
                for i in range(n_nodes):
                    y_pos = 1 + (i + 1) * spacing
                    node_positions[layer].append((x_pos, y_pos))
                    
                    # Different colors for different layers
                    colors = {
                        'input': 'lightblue',
                        'hidden1': 'lightgreen',
                        'hidden2': 'lightgreen',
                        'output': 'salmon'
                    }
                    
                    circle = plt.Circle((x_pos, y_pos), 0.4, fill=True, 
                                       color=colors[layer], alpha=0.7, linewidth=2, 
                                       edgecolor='black')
                    ax.add_patch(circle)
            
            # Connect nodes between layers
            layer_names = list(layer_positions.keys())
            
            for i in range(len(layer_names)-1):
                current_layer = layer_names[i]
                next_layer = layer_names[i+1]
                
                # Draw connections
                for pos1 in node_positions[current_layer]:
                    for pos2 in node_positions[next_layer]:
                        line = plt.Line2D([pos1[0], pos2[0]], [pos1[1], pos2[1]], 
                                         color='gray', alpha=0.5)
                        ax.add_line(line)
            
            # Add annotation for activation function
            plt.text(4.5, 0.5, "Activation Function: ReLU", ha='center', va='center', 
                     fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))
            plt.text(7, 0.5, "Activation Function: ReLU", ha='center', va='center', 
                     fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))
            plt.text(9, 0.5, "Activation Function: Softmax", ha='center', va='center', 
                     fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))
            
            plt.title("Simple Neural Network Architecture", fontsize=16)
        
        draw_neural_network()
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(3)
        plt.close()

# Run the tutorial
if __name__ == "__main__":
    tutorial = AITutorial()
    tutorial.start()