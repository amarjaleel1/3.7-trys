/**
 * Welcome screen functionality for the AI Learning Platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Set up start first lesson button
    const startButton = document.getElementById('start-first-lesson');
    if (startButton) {
        startButton.addEventListener('click', function() {
            // Find first lesson
            const firstLesson = lessons[0];
            if (firstLesson) {
                loadLesson(firstLesson.id);
            }
        });
    }

    // Check if we should show tutorial for new users
    setTimeout(() => {
        const hasSeenTutorial = localStorage.getItem('hasSeenTutorial');
        if (!hasSeenTutorial && !document.querySelector('.modal')) {
            showTutorial();
        }
    }, 2000);
});

// Show interactive tutorial
function showTutorial() {
    // Create tutorial overlay elements
    const overlay = document.createElement('div');
    overlay.className = 'tutorial-overlay';

    // Define steps
    const steps = [
        {
            element: '.sidebar',
            title: 'Lesson Menu',
            content: 'Browse available lessons here. Complete lessons to unlock more advanced topics.',
            position: 'right'
        },
        {
            element: '#coin-display',
            title: 'Earned Coins',
            content: 'You\'ll earn coins by completing lessons. Use them to unlock more advanced content.',
            position: 'bottom'
        },
        {
            element: '#lesson-container',
            title: 'Lesson Content',
            content: 'Each lesson explains a concept and gives you a task to complete.',
            position: 'bottom'
        },
        {
            element: '.welcome-features',
            title: 'Interactive Learning',
            content: 'Write code, visualize results, and earn rewards as you learn.',
            position: 'top'
        }
    ];

    // Start tutorial
    startTutorial(steps);
}

// Run the tutorial
function startTutorial(steps) {
    let currentStep = 0;

    function showStep(step) {
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'tutorial-tooltip ' + step.position;
        tooltip.innerHTML = `
            <div class="tooltip-header">
                <h4>${step.title}</h4>
                <span class="step-counter">${currentStep + 1}/${steps.length}</span>
            </div>
            <div class="tooltip-content">
                <p>${step.content}</p>
            </div>
            <div class="tooltip-actions">
                ${currentStep > 0 ? '<button class="prev-step">Previous</button>' : ''}
                ${currentStep < steps.length - 1 ? 
                    '<button class="next-step">Next</button>' : 
                    '<button class="finish-tutorial">Finish</button>'
                }
            </div>
        `;

        // Position tooltip near target element
        const targetElement = document.querySelector(step.element);
        if (!targetElement) {
            nextStep();
            return;
        }

        document.body.appendChild(tooltip);
        positionTooltip(tooltip, targetElement, step.position);

        // Add highlight to target element
        targetElement.classList.add('tutorial-highlight');

        // Add event listeners to buttons
        if (currentStep > 0) {
            tooltip.querySelector('.prev-step').addEventListener('click', prevStep);
        }

        if (currentStep < steps.length - 1) {
            tooltip.querySelector('.next-step').addEventListener('click', nextStep);
        } else {
            tooltip.querySelector('.finish-tutorial').addEventListener('click', finishTutorial);
        }
    }

    function positionTooltip(tooltip, target, position) {
        const targetRect = target.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        
        // Position based on specified position
        switch (position) {
            case 'top':
                tooltip.style.left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2) + 'px';
                tooltip.style.top = targetRect.top - tooltipRect.height - 10 + 'px';
                break;
            case 'right':
                tooltip.style.left = targetRect.right + 10 + 'px';
                tooltip.style.top = targetRect.top + (targetRect.height / 2) - (tooltipRect.height / 2) + 'px';
                break;
            case 'bottom':
                tooltip.style.left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2) + 'px';
                tooltip.style.top = targetRect.bottom + 10 + 'px';
                break;
            case 'left':
                tooltip.style.left = targetRect.left - tooltipRect.width - 10 + 'px';
                tooltip.style.top = targetRect.top + (targetRect.height / 2) - (tooltipRect.height / 2) + 'px';
                break;
        }

        // Adjust if off-screen
        const tooltipRect2 = tooltip.getBoundingClientRect();
        if (tooltipRect2.left < 0) tooltip.style.left = '10px';
        if (tooltipRect2.right > window.innerWidth) tooltip.style.left = (window.innerWidth - tooltipRect2.width - 10) + 'px';
        if (tooltipRect2.top < 0) tooltip.style.top = '10px';
        if (tooltipRect2.bottom > window.innerHeight) tooltip.style.top = (window.innerHeight - tooltipRect2.height - 10) + 'px';
    }

    function nextStep() {
        clearCurrentStep();
        currentStep++;
        if (currentStep < steps.length) {
            showStep(steps[currentStep]);
        } else {
            finishTutorial();
        }
    }

    function prevStep() {
        clearCurrentStep();
        currentStep--;
        if (currentStep >= 0) {
            showStep(steps[currentStep]);
        } else {
            currentStep = 0;
            showStep(steps[currentStep]);
        }
    }

    function clearCurrentStep() {
        // Remove existing tooltip
        const tooltip = document.querySelector('.tutorial-tooltip');
        if (tooltip) tooltip.remove();

        // Remove highlight from all elements
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });
    }

    function finishTutorial() {
        clearCurrentStep();
        localStorage.setItem('hasSeenTutorial', 'true');
        
        // Show completion message
        showNotification('Tutorial completed! Start with your first lesson.', 'success');
    }

    // Start with first step
    showStep(steps[currentStep]);
}

// Show welcome animation
function animateWelcome() {
    const features = document.querySelectorAll('.feature');
    
    features.forEach((feature, index) => {
        setTimeout(() => {
            feature.classList.add('animated');
        }, 300 * index);
    });

    setTimeout(() => {
        document.querySelector('.cta-button').classList.add('animated');
    }, features.length * 300);
}

// Show animation when page loads
setTimeout(animateWelcome, 500);
