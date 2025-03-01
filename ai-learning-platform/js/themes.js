/**
 * Theme management for AI Learning Platform
 * Supports light and dark themes
 */

// Theme configurations
const themes = {
    light: {
        name: 'light',
        label: 'Light Mode',
        icon: 'fa-sun',
        properties: {
            '--primary-color': '#3498db',
            '--primary-dark': '#2980b9',
            '--secondary-color': '#f1c40f',
            '--dark-bg': '#2c3e50',
            '--darker-bg': '#1a2530',
            '--light-text': '#ecf0f1',
            '--dark-text': '#2c3e50',
            '--success': '#2ecc71',
            '--warning': '#e74c3c',
            '--info': '#3498db',
            '--light-bg': '#f5f5f5',
            '--white': '#ffffff',
            '--code-bg': '#1e1e1e',
            '--code-text': '#d4d4d4'
        }
    },
    dark: {
        name: 'dark',
        label: 'Dark Mode',
        icon: 'fa-moon',
        properties: {
            '--primary-color': '#4ea8e0',
            '--primary-dark': '#2980b9',
            '--secondary-color': '#f1c40f',
            '--dark-bg': '#1a2530',
            '--darker-bg': '#131c24',
            '--light-text': '#ecf0f1',
            '--dark-text': '#ecf0f1',
            '--success': '#2ecc71',
            '--warning': '#e74c3c',
            '--info': '#4ea8e0',
            '--light-bg': '#1e272e',
            '--white': '#2c3e50',
            '--code-bg': '#161616',
            '--code-text': '#e4e4e4'
        }
    }
};

// Initialize theme system
document.addEventListener('DOMContentLoaded', function() {
    setupThemeToggle();
    loadSavedTheme();
});

// Setup theme toggle button
function setupThemeToggle() {
    // Create theme toggle button
    const themeToggle = document.createElement('button');
    themeToggle.className = 'theme-toggle';
    themeToggle.title = 'Toggle theme';
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    
    // Add to UI
    const userInfo = document.querySelector('.user-info');
    if (userInfo) {
        userInfo.appendChild(themeToggle);
        
        // Add click event
        themeToggle.addEventListener('click', toggleTheme);
    }
}

// Load theme from local storage
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme && themes[savedTheme]) {
        applyTheme(savedTheme);
    } else {
        // Check for system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            applyTheme('dark');
        } else {
            applyTheme('light');
        }
    }
}

// Toggle between light and dark theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
}

// Apply theme to document
function applyTheme(themeName) {
    if (!themes[themeName]) {
        console.error(`Theme "${themeName}" not found.`);
        return;
    }
    
    const theme = themes[themeName];
    
    // Set data attribute on html element
    document.documentElement.setAttribute('data-theme', themeName);
    
    // Update theme toggle icon
    const themeToggle = document.querySelector('.theme-toggle i');
    if (themeToggle) {
        themeToggle.className = `fas ${themeName === 'dark' ? 'fa-sun' : 'fa-moon'}`;
    }
    
    // Apply CSS custom properties
    const root = document.documentElement;
    
    for (const [property, value] of Object.entries(theme.properties)) {
        root.style.setProperty(property, value);
    }
    
    // Save preference to local storage
    localStorage.setItem('theme', themeName);
    
    // Dispatch theme change event
    document.dispatchEvent(new CustomEvent('themeChanged', { 
        detail: { theme: themeName }
    }));
    
    // Handle code editor theme if it exists
    updateCodeEditorTheme(themeName);
}

// Update code editor theme
function updateCodeEditorTheme(themeName) {
    const codeEditor = document.getElementById('code-editor');
    
    if (codeEditor) {
        if (themeName === 'dark') {
            codeEditor.style.backgroundColor = '#161616';
            codeEditor.style.color = '#e4e4e4';
        } else {
            codeEditor.style.backgroundColor = '#1e1e1e';
            codeEditor.style.color = '#d4d4d4';
        }
    }
    
    // Update Prism.js theme if loaded
    const prismTheme = document.querySelector('link[href*="prism"]');
    if (prismTheme) {
        const isDark = themeName === 'dark';
        const newThemeUrl = isDark 
            ? 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/themes/prism-tomorrow.min.css'
            : 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/themes/prism.min.css';
        
        if (!prismTheme.href.includes(newThemeUrl)) {
            prismTheme.href = newThemeUrl;
        }
    }
}

// Handle system theme preference changes
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (!localStorage.getItem('theme')) {  // Only auto-change if user hasn't explicitly set a preference
            applyTheme(event.matches ? 'dark' : 'light');
        }
    });
}

// Expose API
window.ThemeManager = {
    toggle: toggleTheme,
    setTheme: applyTheme,
    getCurrentTheme: () => document.documentElement.getAttribute('data-theme') || 'light',
    getAvailableThemes: () => Object.keys(themes)
};
