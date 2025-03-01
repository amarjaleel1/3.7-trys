// Define all lessons
const lessons = [
    {
        id: 'intro',
        title: 'Introduction to AI',
        content: `
            <h3>Welcome to AI Learning!</h3>
            <p>In this course, you'll learn the fundamentals of Artificial Intelligence through interactive lessons and coding exercises.</p>
            <p>Complete tasks to earn coins and unlock more advanced lessons.</p>
            <p>To complete this introduction, write a simple function that prints "Hello AI World!"</p>
        `,
        task: 'Create a function called greetAI() that returns the string "Hello AI World!"',
        hint: 'Your function should use the return keyword, not console.log',
        requiredCoins: 0,
        checkCode: function(code) {
            return code.includes('function greetAI') && code.includes('return') && code.includes('Hello AI World');
        }
    },
    {
        id: 'decision-trees',
        title: 'Decision Trees',
        content: `
            <h3>Decision Trees</h3>
            <p>Decision trees are simple yet powerful algorithms for classification and regression tasks.</p>
            <p>They work by repeatedly splitting the data based on feature values.</p>
            <h4>Task:</h4>
            <p>Implement a simple decision function that classifies data points based on two features:</p>
            <ul>
                <li>If feature1 > 5 and feature2 < 3, classify as "A"</li>
                <li>If feature1 < 5 and feature2 > 7, classify as "B"</li>
                <li>Otherwise, classify as "C"</li>
            </ul>
        `,
        task: 'Create a function called classify(feature1, feature2) that implements the decision tree described above',
        hint: 'Use if-else statements to implement the decision logic',
        requiredCoins: 5,
        checkCode: function(code) {
            return code.includes('function classify') && 
                   code.includes('feature1') && 
                   code.includes('feature2') && 
                   code.includes('return');
        }
    },
    {
        id: 'neural-networks',
        title: 'Neural Networks Basics',
        content: `
            <h3>Neural Networks</h3>
            <p>Neural networks are the foundation of modern deep learning.</p>
            <p>In this lesson, you'll learn about neurons, activation functions, and forward propagation.</p>
            <h4>Task:</h4>
            <p>Implement a single neuron that takes two inputs, has two weights and a bias, and uses the sigmoid activation function.</p>
        `,
        task: 'Create a function neuron(x1, x2, w1, w2, bias) that implements a single neuron with sigmoid activation',
        hint: 'Sigmoid function: f(x) = 1/(1 + Math.exp(-x))',
        requiredCoins: 15,
        checkCode: function(code) {
            return code.includes('function neuron') && 
                   code.includes('Math.exp') && 
                   (code.includes('1/(1+') || code.includes('1 / (1 +'));
        }
    },
    {
        id: 'reinforcement',
        title: 'Reinforcement Learning',
        content: `
            <h3>Reinforcement Learning</h3>
            <p>Reinforcement learning is about training agents to make decisions by rewarding desired behaviors.</p>
            <p>In this lesson, we'll implement a simple Q-learning algorithm.</p>
            <h4>Task:</h4>
            <p>Implement a function that updates a Q-value based on reward and the maximum future Q-value.</p>
        `,
        task: 'Create a function updateQ(currentQ, reward, maxFutureQ, learningRate, discountFactor) that implements the Q-learning update rule',
        hint: 'Q-learning update rule: Q(s,a) = Q(s,a) + learningRate * (reward + discountFactor * maxFutureQ - Q(s,a))',
        requiredCoins: 30,
        checkCode: function(code) {
            return code.includes('function updateQ') && 
                   code.includes('learningRate') && 
                   code.includes('discountFactor');
        }
    }
];

// Initialize lessons in the UI
function initializeLessons() {
    const lessonList = document.getElementById('lesson-list');
    lessonList.innerHTML = '';
    
    lessons.forEach(lesson => {
        const isCompleted = userState.completedLessons.includes(lesson.id);
        const isLocked = lesson.requiredCoins > userState.coins && !isCompleted;
        
        const listItem = document.createElement('li');
        listItem.className = `lesson-item ${isLocked ? 'locked' : ''} ${isCompleted ? 'completed' : ''}`;
        
        if (isLocked) {
            listItem.innerHTML = `${lesson.title} <span class="coin-requirement">(${lesson.requiredCoins} coins)</span>`;
        } else {
            listItem.textContent = lesson.title;
            listItem.addEventListener('click', () => loadLesson(lesson.id));
        }
        
        lessonList.appendChild(listItem);
    });
    
    // If there's a current lesson, load it
    if (userState.currentLesson) {
        loadLesson(userState.currentLesson);
    }
}

// Load a specific lesson
function loadLesson(lessonId) {
    const lesson = lessons.find(l => l.id === lessonId);
    if (!lesson) return;
    
    // Check if lesson is locked
    if (lesson.requiredCoins > userState.coins && !userState.completedLessons.includes(lessonId)) {
        alert(`This lesson requires ${lesson.requiredCoins} coins to unlock.`);
        return;
    }
    
    userState.currentLesson = lessonId;
    saveUserState();
    
    // Update active lesson highlight
    document.querySelectorAll('.lesson-item').forEach(item => {
        item.classList.remove('active');
        if (item.textContent.includes(lesson.title)) {
            item.classList.add('active');
        }
    });
    
    // Update lesson content
    document.getElementById('lesson-title').textContent = lesson.title;
    document.getElementById('lesson-content').innerHTML = lesson.content;
    
    // Show code editor
    document.getElementById('code-container').classList.remove('hidden');
    
    // Reset code editor
    document.getElementById('code-editor').value = '// Write your code here\n\n';
    
    // Show visualization container for relevant lessons
    const visualizationContainer = document.getElementById('visualization-container');
    visualizationContainer.classList.remove('hidden');
    
    // Prepare visualization based on lesson
    prepareVisualization(lesson.id);
}

// Update the lesson list when user state changes
function updateLessonList() {
    initializeLessons();
}
