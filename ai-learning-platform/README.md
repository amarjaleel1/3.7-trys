# AI Learning Platform

An interactive web-based platform for learning AI concepts through visualization, animation, and coding exercises.

![AI Learning Platform Screenshot](screenshots/main-screen.png)

## Features

- **Interactive Lessons**: Learn AI concepts through hands-on coding exercises
- **Dynamic Visualizations**: See your algorithms in action with interactive visualizations
- **Gamification**: Earn coins by completing lessons to unlock more advanced content
- **Progress Tracking**: Track your learning journey with achievements and statistics
- **User Profiles**: Customize your experience and save your progress
- **Code Editor**: Write and execute JavaScript code with syntax highlighting
- **Visual Feedback**: Get immediate visual feedback on your code implementation
- **Hint System**: Stuck on a problem? Use coins to get hints
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Lessons Included

1. **Introduction to AI**
   - Basic concepts and first programming task

2. **Decision Trees**
   - Learn about decision tree algorithms with visual tree representation

3. **Neural Networks Basics**
   - Implement a single neuron with weights and activation function

4. **Reinforcement Learning**
   - Understand Q-learning through interactive grid environment

5. **Additional Lessons** (can be imported)
   - Unsupervised Learning: Clustering
   - Genetic Algorithms
   - Natural Language Processing
   - Computer Vision Basics

## Installation

### Prerequisites

- Node.js (version 14.x or higher)
- Web browser (Chrome, Firefox, Safari, or Edge recommended)

### Setup

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/ai-learning-platform.git
   cd ai-learning-platform
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Start the server
   ```bash
   npm start
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

### Quick Start Scripts

For Windows users:
```bash
run.bat
```

For Mac/Linux users:
```bash
chmod +x run.sh
./run.sh
```

## Development Guide

### Project Structure

- `/css` - Stylesheets
- `/js` - JavaScript files
- `/lessons` - Lesson definitions and additional content
- `/screenshots` - Project screenshots for documentation

### Key Files

- `index.html` - Main application page
- `server.js` - Simple Express server
- `js/main.js` - User state management
- `js/lessons.js` - Lesson content and logic
- `js/visualization.js` - Canvas-based visualizations
- `js/code-editor.js` - Code editor functionality

### Adding New Lessons

1. Create a new lesson object in `lessons/additional_lessons.js`
2. Import and register it in the main lessons array

Example:
```javascript
const newLesson = {
  id: 'your-lesson-id',
  title: 'Your Lesson Title',
  content: `
    <h3>Your Lesson</h3>
    <p>Lesson content goes here...</p>
  `,
  task: 'Description of the coding task',
  hint: 'A helpful hint for the user',
  requiredCoins: 50,
  starterCode: '// Starter code for the user\nfunction yourFunction() {\n  // Code here\n}',
  checkCode: function(code) {
    // Return true if code is correct, false otherwise
    return code.includes('correctPattern');
  }
};
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
