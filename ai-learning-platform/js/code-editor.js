// Code editor enhancements
const codeEditor = document.getElementById('code-editor');

// Simple syntax highlighting (replaced by Prism.js in production)
function highlightSyntax() {
    const code = codeEditor.value;
    // This is a simplified version - Prism.js handles this in the actual implementation
    const highlighted = code
        .replace(/\/\/.+/g, match => `<span class="comment">${match}</span>`)
        .replace(/function\s+\w+/g, match => `<span class="keyword">function</span> <span class="function">${match.split(' ')[1]}</span>`)
        .replace(/return/g, `<span class="keyword">return</span>`)
        .replace(/"[^"]*"/g, match => `<span class="string">${match}</span>`);
    
    return highlighted;
}

// Tab key support in textarea
codeEditor.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        e.preventDefault();
        
        const start = this.selectionStart;
        const end = this.selectionEnd;
        
        // Insert tab at cursor position
        this.value = this.value.substring(0, start) + '  ' + this.value.substring(end);
        
        // Move cursor position after the inserted tab
        this.selectionStart = this.selectionEnd = start + 2;
    }
});

// Auto-save code in progress
let autoSaveTimeout;
codeEditor.addEventListener('input', function() {
    clearTimeout(autoSaveTimeout);
    
    autoSaveTimeout = setTimeout(() => {
        // Save current code to localStorage
        if (userState.currentLesson) {
            localStorage.setItem(`code_${userState.currentLesson}`, this.value);
        }
    }, 1000);
});

// Load previously saved code when switching lessons
function loadSavedCode(lessonId) {
    const savedCode = localStorage.getItem(`code_${lessonId}`);
    if (savedCode) {
        codeEditor.value = savedCode;
    } else {
        // Set default starter code based on lesson
        const lesson = lessons.find(l => l.id === lessonId);
        if (lesson && lesson.starterCode) {
            codeEditor.value = lesson.starterCode;
        } else {
            codeEditor.value = '// Write your code here\n\n';
        }
    }
}

// Template snippets for different lessons
const codeTemplates = {
    'intro': `// Introduction to AI
function greetAI() {
  // Your code here
  
}`,
    'decision-trees': `// Decision Tree Classification
function classify(feature1, feature2) {
  // Your code here
  
}`,
    'neural-networks': `// Neural Network Neuron Implementation
function neuron(x1, x2, w1, w2, bias) {
  // Your code here
  // Remember to use the sigmoid activation function
  
}`,
    'reinforcement': `// Q-Learning Update Rule
function updateQ(currentQ, reward, maxFutureQ, learningRate, discountFactor) {
  // Your code here
  // Implement the Q-learning update rule
  
}`
};

// Code quality checks
function checkCodeQuality(code) {
    const issues = [];
    
    // Check for common issues
    if (code.includes('console.log') && userState.currentLesson === 'intro') {
        issues.push('Use return instead of console.log for this exercise.');
    }
    
    if (code.includes('var ')) {
        issues.push('Consider using let or const instead of var for better variable scoping.');
    }
    
    // Missing semicolons
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line && !line.endsWith('{') && !line.endsWith('}') && 
            !line.endsWith(';') && !line.startsWith('//') && !line.endsWith(':')) {
            issues.push(`Line ${i+1} might be missing a semicolon.`);
        }
    }
    
    return issues;
}

// Initialize editor with templates
function initializeCodeEditor() {
    // Set up initial template based on first lesson
    codeEditor.value = codeTemplates['intro'];
    
    // Add event listener for run button - we already have this in main.js but enhancing it here
    document.getElementById('run-code').addEventListener('click', function() {
        const code = codeEditor.value;
        
        // Check for code quality issues
        const issues = checkCodeQuality(code);
        if (issues.length > 0) {
            const proceed = confirm(`Code quality issues detected:\n\n${issues.join('\n')}\n\nDo you want to run anyway?`);
            if (!proceed) return;
        }
        
        // Now we let the main.js simulateCodeExecution function handle running the code
    });
}

// Update code templates in lessons.js
function updateLessonsWithTemplates() {
    lessons.forEach(lesson => {
        if (codeTemplates[lesson.id]) {
            lesson.starterCode = codeTemplates[lesson.id];
        }
    });
}

// Initialize code editor when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCodeEditor();
    updateLessonsWithTemplates();
});
