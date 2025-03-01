// UI Components and Notifications

// Create notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Add icon based on notification type
    let icon = 'info-circle';
    switch(type) {
        case 'success': icon = 'check-circle'; break;
        case 'warning': icon = 'exclamation-triangle'; break;
        case 'error': icon = 'times-circle'; break;
    }
    
    notification.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    
    // Add to notification container, create if it doesn't exist
    let notificationContainer = document.getElementById('notification-container');
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        document.body.appendChild(notificationContainer);
    }
    
    // Add to DOM
    notificationContainer.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('visible');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('visible');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 4000);
}

// Show hint in a modal
function showHint(hintText) {
    // Create modal container
    const modal = document.createElement('div');
    modal.className = 'modal hint-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="far fa-lightbulb"></i> Hint</h3>
                <button class="close-button">&times;</button>
            </div>
            <div class="hint-content">
                <p>${hintText}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Add event listener to close button
    modal.querySelector('.close-button').addEventListener('click', () => {
        closeModal(modal);
    });
    
    // Close if clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal(modal);
        }
    });
}

// Generic close modal function
function closeModal(modal) {
    modal.classList.remove('show');
    setTimeout(() => {
        modal.remove();
    }, 300);
}

// Animate coin shortage (shake effect)
function animateCoinShortage() {
    const coinDisplay = document.getElementById('coin-display');
    coinDisplay.classList.add('coin-shortage');
    
    setTimeout(() => {
        coinDisplay.classList.remove('coin-shortage');
    }, 500);
}

// Check for daily login reward
function checkDailyLogin() {
    const today = new Date().toISOString().split('T')[0];
    
    if (userState.lastLoginDate !== today) {
        // It's a new day, give login reward
        const isConsecutiveDay = isConsecutiveLogin(userState.lastLoginDate);
        
        if (isConsecutiveDay) {
            userState.streak++;
        } else {
            userState.streak = 1;
        }
        
        // Update last login date
        userState.lastLoginDate = today;
        
        // Calculate reward (more for streak)
        const reward = 5 + Math.min(5, userState.streak);
        
        // Show login reward
        setTimeout(() => {
            showLoginReward(reward, userState.streak);
        }, 1500);
        
        saveUserState();
    }
}

// Check if login is consecutive
function isConsecutiveLogin(lastLogin) {
    if (!lastLogin) return false;
    
    const lastDate = new Date(lastLogin);
    const today = new Date();
    
    // Reset hours to compare just the dates
    lastDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    
    // Calculate difference in days
    const diffTime = today - lastDate;
    const diffDays = Math.round(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays === 1;
}

// Show login reward modal
function showLoginReward(amount, streak) {
    // Create modal container
    const modal = document.createElement('div');
    modal.className = 'modal reward-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-calendar-check"></i> Daily Login Reward</h3>
            </div>
            <div class="login-reward">
                <div class="reward-icon">
                    <i class="fas fa-coins"></i>
                </div>
                <div class="reward-details">
                    <p>You've received <strong>${amount} coins</strong> for logging in today!</p>
                    ${streak > 1 ? `<p class="streak">🔥 ${streak} day streak! Keep it up!</p>` : ''}
                </div>
            </div>
            <button id="claim-reward" class="primary-button">Claim Reward</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Add event listener to claim button
    document.getElementById('claim-reward').addEventListener('click', () => {
        awardCoins(amount, 'Daily login bonus');
        closeModal(modal);
    });
}

// Check for achievements
function checkAchievements() {
    // First lesson completed
    if (userState.completedLessons.length === 1 && !hasAchievement('first_lesson')) {
        addAchievement('first_lesson', 'First Steps', 'Complete your first lesson', 5);
    }
    
    // Complete 3 lessons
    if (userState.completedLessons.length >= 3 && !hasAchievement('three_lessons')) {
        addAchievement('three_lessons', 'Getting Started', 'Complete three lessons', 10);
    }
    
    // Complete all lessons
    if (userState.completedLessons.length >= lessons.length && !hasAchievement('all_lessons')) {
        addAchievement('all_lessons', 'AI Scholar', 'Complete all available lessons', 20);
    }
    
    // Login streak achievements
    if (userState.streak >= 3 && !hasAchievement('three_day_streak')) {
        addAchievement('three_day_streak', 'Consistent Learner', 'Login for 3 days in a row', 10);
    }
}

// Check if user has an achievement
function hasAchievement(id) {
    return userState.achievements.some(a => a.id === id);
}

// Add an achievement
function addAchievement(id, title, description, rewardCoins) {
    const achievement = {
        id,
        title,
        description,
        dateEarned: new Date().toISOString()
    };
    
    userState.achievements.push(achievement);
    saveUserState();
    
    // Show achievement notification
    showAchievementNotification(title, description, rewardCoins);
    
    // Award coins
    if (rewardCoins > 0) {
        awardCoins(rewardCoins, `${title} achievement`);
    }
}

// Show achievement notification
function showAchievementNotification(title, description, rewardCoins) {
    // Create achievement toast
    const toast = document.createElement('div');
    toast.className = 'achievement-toast';
    toast.innerHTML = `
        <div class="achievement-icon">
            <i class="fas fa-trophy"></i>
        </div>
        <div class="achievement-details">
            <h4>Achievement Unlocked!</h4>
            <h3>${title}</h3>
            <p>${description}</p>
            ${rewardCoins ? `<p class="reward">+${rewardCoins} coins</p>` : ''}
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Show with animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 500);
    }, 5000);
}

// Track user progress and show recommendations
function trackProgress() {
    const completedCount = userState.completedLessons.length;
    const totalLessons = lessons.length;
    const progressPercent = Math.round((completedCount / totalLessons) * 100);
    
    // Show progress in profile section if it exists
    const progressElement = document.getElementById('progress-bar');
    if (progressElement) {
        progressElement.style.width = `${progressPercent}%`;
        progressElement.setAttribute('aria-valuenow', progressPercent);
        document.getElementById('progress-percent').textContent = `${progressPercent}%`;
    }
    
    // Show recommendations based on progress
    if (completedCount > 0 && completedCount < totalLessons) {
        // Find next uncompleted lesson
        const nextLesson = lessons.find(lesson => !userState.completedLessons.includes(lesson.id));
        if (nextLesson && progressPercent > 25) {
            showRecommendation(nextLesson);
        }
    }
}

// Show lesson recommendation
function showRecommendation(lesson) {
    const recommendationBox = document.getElementById('recommendation-box');
    if (!recommendationBox) return;
    
    recommendationBox.innerHTML = `
        <h3>Recommended Next Step</h3>
        <div class="recommendation">
            <div class="recommendation-icon">
                <i class="fas fa-forward"></i>
            </div>
            <div class="recommendation-details">
                <h4>${lesson.title}</h4>
                <p>Continue your learning journey with this lesson!</p>
                <button id="go-to-recommendation">Start Lesson</button>
            </div>
        </div>
    `;
    
    recommendationBox.classList.remove('hidden');
    
    // Add event listener to button
    document.getElementById('go-to-recommendation').addEventListener('click', () => {
        loadLesson(lesson.id);
        recommendationBox.classList.add('hidden');
    });
}
