// User state management
let userState = {
    username: "Guest",
    coins: 0,
    completedLessons: [],
    currentLesson: null,
    achievements: [],
    lastLoginDate: null,
    streak: 0
};

// Load user state from local storage if available
function loadUserState() {
    const savedState = localStorage.getItem('aiLearningUserState');
    if (savedState) {
        userState = JSON.parse(savedState);
        
        // Handle case where saved state might be missing new properties
        if (!userState.achievements) userState.achievements = [];
        if (!userState.lastLoginDate) userState.lastLoginDate = new Date().toISOString().split('T')[0];
        if (!userState.streak) userState.streak = 0;
        
        updateUI();
    } else {
        // First time user - show welcome modal
        setTimeout(() => {
            showWelcomeModal();
        }, 1000);
    }
}

// Save user state to local storage
function saveUserState() {
    localStorage.setItem('aiLearningUserState', JSON.stringify(userState));
}

// Update UI with current user state
function updateUI() {
    document.getElementById('username').textContent = userState.username;
    document.getElementById('coins').textContent = userState.coins;
    
    // Update lesson list
    updateLessonList();
}

// Award coins to the user
function awardCoins(amount, reason = '') {
    userState.coins += amount;
    updateUI();
    
    // Show animation and notification
    const coinElement = document.getElementById('coin-display');
    coinElement.classList.add('coin-animation');
    setTimeout(() => {
        coinElement.classList.remove('coin-animation');
    }, 1000);
    
    showNotification(`+${amount} coins${reason ? ' - ' + reason : ''}`, 'success');
    
    saveUserState();
}

// Complete a lesson
function completeLesson(lessonId) {
    if (!userState.completedLessons.includes(lessonId)) {
        userState.completedLessons.push(lessonId);
        
        // Find the lesson in the list and add 'just-completed' class
        const lessonItems = document.querySelectorAll('.lesson-item');
        lessonItems.forEach(item => {
            if (item.dataset.lessonId === lessonId) {
                item.classList.add('just-completed');
                setTimeout(() => {
                    item.classList.remove('just-completed');
                }, 2000);
            }
        });
        
        // Award coins
        const rewardCoins = 10;
        awardCoins(rewardCoins, 'Lesson completed');
        
        // Check for achievements
        checkAchievements();
        
        // Update UI
        updateLessonList();
        saveUserState();
        
        // Show completion modal
        showCompletionModal(lessonId);
    }
}

// Handle run code button
document.getElementById('run-code').addEventListener('click', function() {
    const code = document.getElementById('code-editor').value;
    if (code.trim() === '') return;

    try {
        // For safety, we're not actually executing user code
        // Instead, we simulate execution based on the current lesson
        simulateCodeExecution(code);
    } catch (e) {
        alert('Error: ' + e.message);
    }
});

// Handle hint button
document.getElementById('get-hint').addEventListener('click', function() {
    if (userState.coins < 5) {
        alert('Not enough coins! Hints cost 5 coins.');
        return;
    }
    
    const currentLesson = lessons.find(l => l.id === userState.currentLesson);
    if (currentLesson && currentLesson.hint) {
        alert(currentLesson.hint);
        userState.coins -= 5;
        updateUI();
        saveUserState();
    } else {
        alert('No hint available for this lesson.');
    }
});

// Simulate code execution based on lesson objectives
function simulateCodeExecution(code) {
    const currentLesson = lessons.find(l => l.id === userState.currentLesson);
    if (!currentLesson) return;
    
    // Check if code meets the lesson objectives (simplified)
    if (currentLesson.checkCode && currentLesson.checkCode(code)) {
        visualizeResults(code, currentLesson);
        completeLesson(currentLesson.id);
        alert('Great job! You completed the lesson and earned 10 coins!');
    } else {
        alert('Your solution doesn\'t meet the lesson objectives. Try again!');
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    loadUserState();
    initializeLessons();
    setupEventListeners();
    checkDailyLogin();
    
    // Show welcome animation
    setTimeout(() => {
        document.querySelector('.logo').classList.add('animated');
    }, 300);
});

// Set up event listeners
function setupEventListeners() {
    // Run code button
    document.getElementById('run-code').addEventListener('click', function() {
        const code = document.getElementById('code-editor').value;
        if (code.trim() === '') {
            showNotification('Please write some code first', 'warning');
            return;
        }

        try {
            simulateCodeExecution(code);
        } catch (e) {
            showNotification('Error: ' + e.message, 'error');
        }
    });
    
    // Get hint button
    document.getElementById('get-hint').addEventListener('click', function() {
        if (userState.coins < 5) {
            showNotification('Not enough coins! Hints cost 5 coins', 'warning');
            animateCoinShortage();
            return;
        }
        
        const currentLesson = lessons.find(l => l.id === userState.currentLesson);
        if (currentLesson && currentLesson.hint) {
            showHint(currentLesson.hint);
            userState.coins -= 5;
            updateUI();
            saveUserState();
        } else {
            showNotification('No hint available for this lesson', 'info');
        }
    });
}

// Welcome modal for first-time users
function showWelcomeModal() {
    // Create modal container
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>Welcome to AI Learning Platform!</h2>
            <p>This interactive platform will help you learn AI concepts through hands-on coding exercises.</p>
            <p>Complete tasks to earn coins and unlock more advanced lessons.</p>
            <div class="name-input">
                <label for="username-input">What should we call you?</label>
                <input type="text" id="username-input" placeholder="Enter your name" maxlength="20">
            </div>
            <button id="start-learning">Start Learning</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Focus on input
    setTimeout(() => {
        document.getElementById('username-input').focus();
    }, 100);
    
    // Add event listener to start button
    document.getElementById('start-learning').addEventListener('click', function() {
        const name = document.getElementById('username-input').value.trim();
        if (name) {
            userState.username = name;
        }
        
        // Remove modal
        modal.classList.add('closing');
        setTimeout(() => {
            document.body.removeChild(modal);
        }, 300);
        
        // Save user state
        saveUserState();
        updateUI();
        
        // Award initial coins as welcome gift
        awardCoins(10, 'Welcome gift');
    });
}

// Show lesson completion modal
function showCompletionModal(lessonId) {
    const lesson = lessons.find(l => l.id === lessonId);
    if (!lesson) return;
    
    // Create modal container
    const modal = document.createElement('div');
    modal.className = 'modal completion-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="completion-header">
                <i class="fas fa-check-circle"></i>
                <h2>Lesson Completed!</h2>
            </div>
            <p>You've successfully completed the "${lesson.title}" lesson.</p>
            <div class="reward-info">
                <p><i class="fas fa-coins"></i> +10 coins awarded</p>
            </div>
            <div class="next-actions">
                <button id="next-lesson">Next Lesson</button>
                <button id="close-modal" class="secondary">Close</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Find next lesson
    const currentLessonIndex = lessons.findIndex(l => l.id === lessonId);
    const nextLesson = lessons[currentLessonIndex + 1];
    
    // Add event listeners
    document.getElementById('close-modal').addEventListener('click', function() {
        closeModal();
    });
    
    document.getElementById('next-lesson').addEventListener('click', function() {
        closeModal();
        if (nextLesson) {
            loadLesson(nextLesson.id);
        } else {
            showNotification('You completed all available lessons!', 'success');
        }
    });
    
    function closeModal() {
        modal.classList.add('closing');
        setTimeout(() => {
            document.body.removeChild(modal);
        }, 300);
    }
}
