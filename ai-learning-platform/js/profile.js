// User profile management

// Initialize user profile when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupProfileButton();
});

// Set up profile button in header
function setupProfileButton() {
    const userInfo = document.querySelector('.user-info');
    
    // Create profile button
    const profileButton = document.createElement('button');
    profileButton.id = 'profile-button';
    profileButton.className = 'profile-button';
    profileButton.innerHTML = `<i class="fas fa-user"></i>`;
    profileButton.title = 'View Profile';
    
    userInfo.appendChild(profileButton);
    
    // Add click event
    profileButton.addEventListener('click', showProfileModal);
}

// Show profile modal
function showProfileModal() {
    // Create modal container
    const modal = document.createElement('div');
    modal.className = 'modal profile-modal';
    modal.innerHTML = `
        <div class="modal-content profile-content">
            <div class="modal-header">
                <h3><i class="fas fa-user-circle"></i> User Profile</h3>
                <button class="close-button">&times;</button>
            </div>
            <div class="profile-body">
                <div class="profile-section">
                    <div class="username-display">
                        <div class="avatar">${getUserInitials()}</div>
                        <div class="user-details">
                            <h4>${userState.username}</h4>
                            <button id="edit-username" class="small-button">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h4>Learning Progress</h4>
                    <div class="progress-container">
                        <div class="progress-bar" id="progress-bar" role="progressbar" 
                             style="width: ${calculateProgress()}%;" 
                             aria-valuenow="${calculateProgress()}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                        </div>
                    </div>
                    <div class="progress-stats">
                        <span id="progress-percent">${calculateProgress()}%</span> completed
                        <span class="lessons-count">${userState.completedLessons.length} of ${lessons.length} lessons</span>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h4>Stats</h4>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value">${userState.coins}</div>
                            <div class="stat-label">Coins</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${userState.completedLessons.length}</div>
                            <div class="stat-label">Lessons</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${userState.achievements.length}</div>
                            <div class="stat-label">Achievements</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${userState.streak}</div>
                            <div class="stat-label">Day Streak</div>
                        </div>
                    </div>
                </div>
                
                <div class="profile-section">
                    <h4>Achievements</h4>
                    <div class="achievements-list">
                        ${renderAchievements()}
                    </div>
                </div>
                
                <div class="profile-actions">
                    <button id="reset-progress" class="danger-button">
                        <i class="fas fa-trash-alt"></i> Reset Progress
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Add event listeners
    modal.querySelector('.close-button').addEventListener('click', () => {
        closeModal(modal);
    });
    
    // Edit username button
    document.getElementById('edit-username').addEventListener('click', () => {
        showEditUsernameForm();
    });
    
    // Reset progress button
    document.getElementById('reset-progress').addEventListener('click', () => {
        confirmResetProgress(modal);
    });
}

// Calculate progress percentage
function calculateProgress() {
    return Math.round((userState.completedLessons.length / lessons.length) * 100);
}

// Get user initials for avatar
function getUserInitials() {
    if (userState.username === 'Guest') return 'G';
    
    const words = userState.username.split(' ');
    if (words.length === 1) {
        return words[0][0].toUpperCase();
    } else {
        return (words[0][0] + words[1][0]).toUpperCase();
    }
}

// Render achievements list
function renderAchievements() {
    if (userState.achievements.length === 0) {
        return '<div class="no-achievements">No achievements yet. Complete lessons to earn achievements!</div>';
    }
    
    return userState.achievements.map(achievement => `
        <div class="achievement-item">
            <div class="achievement-icon">
                <i class="fas fa-trophy"></i>
            </div>
            <div class="achievement-info">
                <h5>${achievement.title}</h5>
                <p>${achievement.description}</p>
                <span class="date-earned">${formatDate(achievement.dateEarned)}</span>
            </div>
        </div>
    `).join('');
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

// Show edit username form
function showEditUsernameForm() {
    // Create edit form modal
    const modal = document.createElement('div');
    modal.className = 'modal edit-username-modal';
    modal.innerHTML = `
        <div class="modal-content small-modal">
            <div class="modal-header">
                <h3>Edit Username</h3>
                <button class="close-button">&times;</button>
            </div>
            <div class="edit-form">
                <div class="form-group">
                    <label for="new-username">New Username</label>
                    <input type="text" id="new-username" value="${userState.username}" maxlength="20">
                </div>
                <div class="form-actions">
                    <button id="save-username" class="primary-button">Save</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Focus on input
    setTimeout(() => {
        document.getElementById('new-username').focus();
    }, 100);
    
    // Add event listeners
    modal.querySelector('.close-button').addEventListener('click', () => {
        closeModal(modal);
    });
    
    document.getElementById('save-username').addEventListener('click', () => {
        const newUsername = document.getElementById('new-username').value.trim();
        if (newUsername) {
            userState.username = newUsername;
            saveUserState();
            updateUI();
            closeModal(modal);
            
            // Update profile modal if open
            const profileContent = document.querySelector('.profile-content');
            if (profileContent) {
                profileContent.querySelector('.username-display h4').textContent = newUsername;
                profileContent.querySelector('.avatar').textContent = getUserInitials();
            }
            
            showNotification('Username updated successfully', 'success');
        } else {
            showNotification('Username cannot be empty', 'warning');
        }
    });
}

// Confirm reset progress
function confirmResetProgress(parentModal) {
    // Create confirmation modal
    const modal = document.createElement('div');
    modal.className = 'modal confirm-modal';
    modal.innerHTML = `
        <div class="modal-content small-modal">
            <div class="modal-header">
                <h3>Reset Progress</h3>
                <button class="close-button">&times;</button>
            </div>
            <div class="confirm-content">
                <p class="warning-text">
                    <i class="fas fa-exclamation-triangle"></i>
                    Are you sure you want to reset all your progress?
                </p>
                <p>This action cannot be undone.</p>
                <div class="confirm-actions">
                    <button id="confirm-reset" class="danger-button">Reset Progress</button>
                    <button id="cancel-reset" class="secondary-button">Cancel</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Add event listeners
    modal.querySelector('.close-button').addEventListener('click', () => {
        closeModal(modal);
    });
    
    document.getElementById('cancel-reset').addEventListener('click', () => {
        closeModal(modal);
    });
    
    document.getElementById('confirm-reset').addEventListener('click', () => {
        // Reset user state but keep username
        const username = userState.username;
        userState = {
            username: username,
            coins: 0,
            completedLessons: [],
            currentLesson: null,
            achievements: [],
            lastLoginDate: new Date().toISOString().split('T')[0],
            streak: 0
        };
        
        saveUserState();
        updateUI();
        
        // Close both modals
        closeModal(modal);
        closeModal(parentModal);
        
        showNotification('Your progress has been reset', 'info');
    });
}
