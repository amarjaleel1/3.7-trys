/**
 * Tutorial functionality for the AI Learning Platform
 */

// Tutorial data
const tutorialData = {
    hasShown: false,
    steps: [
        {
            element: '.sidebar',
            title: 'Lesson Menu',
            content: 'Browse available lessons here. Complete lessons to unlock more advanced topics.',
            position: 'right'
        },
        {
            element: '#coin-display',
            title: 'Earned Coins',
            content: 'You\'ll earn coins by completing lessons. Use them to unlock more advanced content or buy hints when you\'re stuck.',
            position: 'bottom'
        },
        {
            element: '#code-container',
            title: 'Code Editor',
            content: 'Write your solutions here. Press Ctrl+Enter to run your code quickly.',
            position: 'top'
        },
        {
            element: '#visualization-container',
            title: 'Visualization Area',
            content: 'See your algorithms in action! This area shows visual representations of your code execution.',
            position: 'top'
        }
    ]
};

// Initialize tutorial when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add tutorial button to header
    setupTutorialButton();
});

// Show tutorial initialization
function setupTutorialButton() {
    const userInfo = document.querySelector('.user-info');
    
    if (userInfo) {
        // Create tutorial button
        const tutorialButton = document.createElement('button');
        tutorialButton.className = 'tutorial-button';
        tutorialButton.title = 'Show Tutorial';
        tutorialButton.innerHTML = '<i class="fas fa-question-circle"></i>';
        
        // Add button to DOM
        userInfo.appendChild(tutorialButton);
        
        // Add click event
        tutorialButton.addEventListener('click', function() {
            startTutorial();
        });
    }
}

// Start the tutorial
function startTutorial(customSteps = null) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'tutorial-overlay';
    document.body.appendChild(overlay);
    
    // Track current step
    let currentStep = 0;
    
    // Use custom steps or default steps
    const steps = customSteps || tutorialData.steps;
    
    // Show the current step
    function showCurrentStep() {
        const step = steps[currentStep];
        
        // Find target element
        const targetElement = document.querySelector(step.element);
        if (!targetElement) {
            // Skip this step if element not found
            goToNextStep();
            return;
        }
        
        // Create tooltip
        createTooltip(step, targetElement);
    }
    
    // Create tooltip for a step
    function createTooltip(step, targetElement) {
        // Remove any existing tooltips
        const existingTooltip = document.querySelector('.tutorial-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }
        
        // Remove existing highlights
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });
        
        // Create new tooltip
        const tooltip = document.createElement('div');
        tooltip.className = `tutorial-tooltip ${step.position || 'bottom'}`;
        tooltip.innerHTML = `
            <div class="tooltip-header">
                <h4>${step.title}</h4>
                <span class="step-counter">${currentStep + 1}/${steps.length}</span>
            </div>
            <div class="tooltip-content">
                <p>${step.content}</p>
            </div>
            <div class="tooltip-actions">
                ${currentStep > 0 ? 
                    '<button class="prev-step">Previous</button>' : 
                    ''}
                ${currentStep < steps.length - 1 ? 
                    '<button class="next-step">Next</button>' : 
                    '<button class="finish-tutorial">Finish</button>'}
            </div>
        `;
        
        // Add tooltip to DOM
        document.body.appendChild(tooltip);
        
        // Highlight target element
        targetElement.classList.add('tutorial-highlight');
        
        // Position tooltip relative to target
        positionTooltip(tooltip, targetElement, step.position || 'bottom');
        
        // Add event listeners
        if (currentStep > 0) {
            tooltip.querySelector('.prev-step').addEventListener('click', goToPrevStep);
        }
        
        if (currentStep < steps.length - 1) {
            tooltip.querySelector('.next-step').addEventListener('click', goToNextStep);
        } else {
            tooltip.querySelector('.finish-tutorial').addEventListener('click', endTutorial);
        }
    }
    
    // Position tooltip relative to target element
    function positionTooltip(tooltip, targetElement, position) {
        const targetRect = targetElement.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        
        // Calculate positions
        let top, left;
        
        switch (position) {
            case 'top':
                left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);
                top = targetRect.top - tooltipRect.height - 15;
                break;
            case 'right':
                left = targetRect.right + 15;
                top = targetRect.top + (targetRect.height / 2) - (tooltipRect.height / 2);
                break;
            case 'bottom':
                left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);
                top = targetRect.bottom + 15;
                break;
            case 'left':
                left = targetRect.left - tooltipRect.width - 15;
                top = targetRect.top + (targetRect.height / 2) - (tooltipRect.height / 2);
                break;
        }
        
        // Apply position
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
        
        // Ensure tooltip is visible in viewport
        const tooltipUpdatedRect = tooltip.getBoundingClientRect();
        
        // Adjust if off-screen
        if (tooltipUpdatedRect.left < 10) {
            tooltip.style.left = '10px';
        }
        
        if (tooltipUpdatedRect.right > window.innerWidth - 10) {
            tooltip.style.left = `${window.innerWidth - tooltipUpdatedRect.width - 10}px`;
        }
        
        if (tooltipUpdatedRect.top < 10) {
            tooltip.style.top = '10px';
        }
        
        if (tooltipUpdatedRect.bottom > window.innerHeight - 10) {
            tooltip.style.top = `${window.innerHeight - tooltipUpdatedRect.height - 10}px`;
        }
    }
    
    // Go to next step
    function goToNextStep() {
        currentStep++;
        
        if (currentStep < steps.length) {
            showCurrentStep();
        } else {
            endTutorial();
        }
    }
    
    // Go to previous step
    function goToPrevStep() {
        currentStep--;
        
        if (currentStep >= 0) {
            showCurrentStep();
        } else {
            currentStep = 0;
            showCurrentStep();
        }
    }
    
    // End the tutorial
    function endTutorial() {
        // Remove overlay
        overlay.remove();
        
        // Remove any tooltips
        const tooltip = document.querySelector('.tutorial-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
        
        // Remove highlights
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });
        
        // Mark tutorial as shown
        tutorialData.hasShown = true;
        localStorage.setItem('hasSeenTutorial', 'true');
        
        // Show completion message
        if (typeof showNotification === 'function') {
            showNotification('Tutorial completed! Start exploring the platform.', 'success');
        }
    }
    
    // Start tutorial with first step
    showCurrentStep();
}
