/**
 * Analytics module for the AI Learning Platform
 * Collects anonymous usage data to improve the platform
 */

// Analytics state
const analyticsState = {
    initialized: false,
    sessionId: generateSessionId(),
    events: [],
    settings: {
        collectAnonymousData: true,
        shareProgress: false
    }
};

// Initialize analytics
function initAnalytics() {
    if (analyticsState.initialized) return;
    
    // Load settings from localStorage
    const savedSettings = localStorage.getItem('analyticsSettings');
    if (savedSettings) {
        try {
            analyticsState.settings = JSON.parse(savedSettings);
        } catch (e) {
            console.error('Error parsing analytics settings:', e);
        }
    }
    
    // Show opt-in dialog if first time
    if (!localStorage.getItem('analyticsOptIn')) {
        setTimeout(showAnalyticsOptIn, 5000);
    }
    
    // Set up event listeners
    setupAnalyticsEvents();
    
    analyticsState.initialized = true;
    
    // Track session start
    trackEvent('session_start', {
        referrer: document.referrer,
        userAgent: navigator.userAgent
    });
}

// Generate unique session ID
function generateSessionId() {
    return 'xxxx-xxxx-xxxx-xxxx'.replace(/x/g, () => {
        return Math.floor(Math.random() * 16).toString(16);
    });
}

// Set up event listeners for tracking
function setupAnalyticsEvents() {
    // Track lesson views
    document.addEventListener('lessonLoaded', function(e) {
        if (!analyticsState.settings.collectAnonymousData) return;
        
        trackEvent('lesson_view', {
            lessonId: e.detail.lessonId,
            lessonTitle: e.detail.lessonTitle
        });
    });
    
    // Track code executions
    document.addEventListener('codeExecuted', function(e) {
        if (!analyticsState.settings.collectAnonymousData) return;
        
        trackEvent('code_executed', {
            lessonId: e.detail.lessonId,
            success: e.detail.success,
            codeLength: e.detail.codeLength
        });
    });
    
    // Track hint requests
    document.addEventListener('hintRequested', function(e) {
        if (!analyticsState.settings.collectAnonymousData) return;
        
        trackEvent('hint_requested', {
            lessonId: e.detail.lessonId
        });
    });
}

// Track an event
function trackEvent(eventName, data = {}) {
    if (!analyticsState.settings.collectAnonymousData) return;
    
    // Add event to local storage
    const event = {
        eventName,
        timestamp: new Date().toISOString(),
        sessionId: analyticsState.sessionId,
        ...data
    };
    
    analyticsState.events.push(event);
    
    // Send events if we have enough
    if (analyticsState.events.length >= 10) {
        sendEvents();
    }
}

// Send collected events to server
function sendEvents() {
    if (!analyticsState.settings.collectAnonymousData || analyticsState.events.length === 0) return;
    
    // In a real application, you would send the data to your server
    // For this example, we'll just log to console and clear the queue
    console.log('Analytics events:', analyticsState.events);
    
    // Clear the queue after sending
    analyticsState.events = [];
}

// Show opt-in dialog for analytics
function showAnalyticsOptIn() {
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'modal analytics-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Help Us Improve</h3>
            </div>
            <div class="analytics-content">
                <p>Would you like to help us improve the AI Learning Platform by sharing anonymous usage data?</p>
                <p class="privacy-note">We only collect information about lesson usage and feature interactions. We never collect personal information or the code you write.</p>
                
                <div class="analytics-options">
                    <div class="option">
                        <label class="toggle">
                            <input type="checkbox" id="collect-data" checked>
                            <span class="toggle-slider"></span>
                        </label>
                        <div class="option-text">
                            <h4>Collect anonymous usage data</h4>
                            <p>Help us understand how lessons are used</p>
                        </div>
                    </div>
                    
                    <div class="option">
                        <label class="toggle">
                            <input type="checkbox" id="share-progress">
                            <span class="toggle-slider"></span>
                        </label>
                        <div class="option-text">
                            <h4>Share progress anonymously</h4>
                            <p>Help others by contributing to community stats</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="analytics-actions">
                <button id="save-analytics-settings" class="primary-button">Save Preferences</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Show modal
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Add event listeners
    document.getElementById('save-analytics-settings').addEventListener('click', function() {
        const collectData = document.getElementById('collect-data').checked;
        const shareProgress = document.getElementById('share-progress').checked;
        
        analyticsState.settings.collectAnonymousData = collectData;
        analyticsState.settings.shareProgress = shareProgress;
        
        localStorage.setItem('analyticsSettings', JSON.stringify(analyticsState.settings));
        localStorage.setItem('analyticsOptIn', 'true');
        
        closeModal(modal);
        
        showNotification('Preferences saved. Thank you!', 'success');
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initAnalytics);

// Ensure events are sent before page unload
window.addEventListener('beforeunload', function() {
    sendEvents();
});

// Export functions
window.AI_Analytics = {
    trackEvent,
    showSettings: showAnalyticsOptIn
};
