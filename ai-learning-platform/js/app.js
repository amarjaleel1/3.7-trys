/**
 * Main application initialization
 * Connects all components and sets up event listeners
 */

// App state
const appState = {
    initialized: false,
    version: '1.0.0',
    debug: false,
    theme: 'light'
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Main initialization function
function initializeApp() {
    if (appState.initialized) return;
    
    console.log(`AI Learning Platform v${appState.version} initializing...`);
    
    // Check URL parameters for options
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('debug')) {
        appState.debug = urlParams.get('debug') === 'true';
    }
    
    if (urlParams.has('theme')) {
        setTheme(urlParams.get('theme'));
    }
    
    // Set up global event listeners
    setupGlobalEventListeners();
    
    // Set up analytics settings link
    document.getElementById('show-analytics-settings')?.addEventListener('click', function(e) {
        e.preventDefault();
        if (window.AI_Analytics && window.AI_Analytics.showSettings) {
            window.AI_Analytics.showSettings();
        }
    });
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Check if we need to load a specific lesson from URL
    if (urlParams.has('lesson')) {
        const lessonId = urlParams.get('lesson');
        // Wait for lessons to be initialized
        setTimeout(() => {
            loadLesson(lessonId);
        }, 500);
    }
    
    appState.initialized = true;
    console.log('AI Learning Platform initialized successfully');
    
    // Dispatch app initialized event
    window.dispatchEvent(new CustomEvent('app-initialized'));
}

// Set up global event listeners
function setupGlobalEventListeners() {
    // Track errors
    window.addEventListener('error', function(e) {
        console.error('Application error:', e.error);
        
        if (appState.debug) {
            showNotification('Error: ' + e.error.message, 'error');
        }
        
        // Track in analytics
        if (window.AI_Analytics && window.AI_Analytics.trackEvent) {
            window.AI_Analytics.trackEvent('app_error', {
                message: e.error.message,
                source: e.filename,
                line: e.lineno,
                column: e.colno
            });
        }
    });
    
    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled promise rejection:', e.reason);
        
        if (appState.debug) {
            showNotification('Promise error: ' + e.reason, 'error');
        }
    });
    
    // Handle window resize for visualizations
    window.addEventListener('resize', debounce(function() {
        // Resize canvas if visualization is active
        const canvas = document.getElementById('visualization-canvas');
        if (canvas && visualizationState && visualizationState.type) {
            // Adjust canvas size
            adjustCanvasSize();
            
            // Redraw visualization
            switch(visualizationState.type) {
                case 'intro':
                    drawIntroVisualization();
                    break;
                case 'decision-tree':
                    drawDecisionTree();
                    break;
                case 'neural-network':
                    drawNeuralNetwork();
                    break;
                case 'reinforcement':
                    drawRLEnvironment();
                    break;
            }
        }
    }, 250));
    
    // Handle theme toggle if it exists
    document.querySelector('.theme-toggle')?.addEventListener('click', function() {
        toggleTheme();
    });
}

// Set application theme
function setTheme(theme) {
    if (theme !== 'light' && theme !== 'dark') {
        theme = 'light'; // Default to light
    }
    
    document.body.setAttribute('data-theme', theme);
    appState.theme = theme;
    localStorage.setItem('theme', theme);
}

// Toggle between light and dark theme
function toggleTheme() {
    const newTheme = appState.theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to run code
        if (e.ctrlKey && e.key === 'Enter') {
            if (!document.getElementById('code-container').classList.contains('hidden')) {
                document.getElementById('run-code').click();
            }
        }
        
        // Alt+H for hint
        if (e.altKey && e.key === 'h') {
            if (!document.getElementById('code-container').classList.contains('hidden')) {
                document.getElementById('get-hint').click();
            }
        }
        
        // Toggle debug mode with Ctrl+Shift+D
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
            appState.debug = !appState.debug;
            showNotification('Debug mode: ' + (appState.debug ? 'enabled' : 'disabled'), 'info');
        }
    });
}

// Adjust canvas size based on container
function adjustCanvasSize() {
    const canvas = document.getElementById('visualization-canvas');
    const container = document.getElementById('visualization-container');
    
    if (canvas && container) {
        const containerWidth = container.clientWidth - 30; // Adjust for padding
        
        // Set canvas width while maintaining aspect ratio
        canvas.width = containerWidth;
        canvas.height = containerWidth * 0.6; // Maintain 5:3 aspect ratio
        
        // Reset context after resize
        if (ctx) {
            ctx = canvas.getContext('2d');
        }
    }
}

// Create a debounce function for handling resize events
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            func.apply(context, args);
        }, wait);
    };
}

// Handle loading screen
function showLoadingScreen() {
    const loader = document.createElement('div');
    loader.className = 'loading-screen';
    loader.innerHTML = `
        <div class="loader-content">
            <div class="loader-spinner"></div>
            <p>Loading AI Learning Platform...</p>
        </div>
    `;
    
    document.body.appendChild(loader);
    
    return {
        hide: function() {
            loader.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(loader);
            }, 500);
        }
    };
}

// Display system message in notification center
function showSystemMessage(title, message) {
    const notification = document.createElement('div');
    notification.className = 'system-notification';
    notification.innerHTML = `
        <h3>${title}</h3>
        <p>${message}</p>
        <button class="close-notification">Dismiss</button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    notification.querySelector('.close-notification').addEventListener('click', () => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
}

// Show welcome message for new users (only once)
function showWelcomeMessage() {
    if (!localStorage.getItem('welcomeMessageSeen')) {
        setTimeout(() => {
            showSystemMessage(
                'Welcome to AI Learning Platform!', 
                'Start your journey into AI by selecting a lesson from the sidebar. Complete tasks to earn coins and unlock more advanced content!'
            );
            localStorage.setItem('welcomeMessageSeen', 'true');
        }, 3000);
    }
}

// Initialize loading screen
const loader = showLoadingScreen();

// Hide loading screen after everything is loaded
window.addEventListener('load', function() {
    setTimeout(() => {
        loader.hide();
        showWelcomeMessage();
    }, 500);
});
