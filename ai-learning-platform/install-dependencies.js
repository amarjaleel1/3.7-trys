/**
 * AI Learning Platform - Dependencies Installer
 * 
 * This script helps to install all the necessary dependencies for the AI Learning Platform.
 * It provides a user-friendly console interface.
 */
 
const { execSync } = require('child_process');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

// Create readline interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Console colors
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    dim: '\x1b[2m',
    underscore: '\x1b[4m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

// Welcome message
function showWelcome() {
    console.log(`
${colors.bright}${colors.cyan}===============================================${colors.reset}
${colors.bright}${colors.cyan}    AI Learning Platform - Setup Assistant${colors.reset}
${colors.bright}${colors.cyan}===============================================${colors.reset}

This assistant will help you set up all dependencies 
required for the AI Learning Platform.

`);
}

// Check Node.js version
function checkNodeVersion() {
    try {
        const nodeVersion = execSync('node -v').toString().trim();
        console.log(`${colors.bright}Node.js Version:${colors.reset} ${nodeVersion}`);
        
        // Extract version number
        const versionMatch = nodeVersion.match(/v(\d+)\./);
        if (versionMatch) {
            const majorVersion = parseInt(versionMatch[1]);
            
            if (majorVersion < 14) {
                console.log(`
${colors.yellow}Warning:${colors.reset} The detected Node.js version might be too old.
We recommend using Node.js version 14 or newer.
You can download the latest version from https://nodejs.org/
`);
            } else {
                console.log(`${colors.green}✓ Node.js version is compatible${colors.reset}`);
            }
        }
    } catch (error) {
        console.log(`
${colors.red}Error:${colors.reset} Node.js is not installed or not in your PATH.
Please install Node.js from https://nodejs.org/
`);
        process.exit(1);
    }
}

// Check NPM version
function checkNpmVersion() {
    try {
        const npmVersion = execSync('npm -v').toString().trim();
        console.log(`${colors.bright}NPM Version:${colors.reset} ${npmVersion}`);
        console.log(`${colors.green}✓ NPM is available${colors.reset}`);
    } catch (error) {
        console.log(`
${colors.red}Error:${colors.reset} NPM is not installed or not working properly.
NPM should come bundled with Node.js. Please reinstall Node.js.
`);
        process.exit(1);
    }
}

// Install dependencies
function installDependencies() {
    console.log(`
${colors.bright}Installing dependencies...${colors.reset}
This may take a few minutes.
`);
    
    try {
        execSync('npm install', { stdio: 'inherit' });
        console.log(`
${colors.green}✓ Dependencies installed successfully!${colors.reset}
`);
    } catch (error) {
        console.log(`
${colors.red}Error:${colors.reset} Failed to install dependencies.
Error message: ${error.message}

Try running 'npm install' manually.
`);
        process.exit(1);
    }
}

// Check if the platform is ready to run
function checkReadiness() {
    if (!fs.existsSync(path.join(__dirname, 'node_modules'))) {
        return false;
    }
    
    try {
        // Check for express module
        require.resolve('express');
        return true;
    } catch (error) {
        return false;
    }
}

// Run the platform
function runPlatform() {
    rl.question(`
${colors.bright}Would you like to start the AI Learning Platform now? (y/n)${colors.reset} `, (answer) => {
        if (answer.toLowerCase() === 'y') {
            console.log(`
${colors.bright}Starting the AI Learning Platform...${colors.reset}

When the server is running, open your browser and go to:
${colors.cyan}http://localhost:3000${colors.reset}

Press Ctrl+C to stop the server
`);
            try {
                execSync('npm start', { stdio: 'inherit' });
            } catch (error) {
                // This will trigger if the user presses Ctrl+C to exit
            }
        } else {
            console.log(`
${colors.bright}Setup complete.${colors.reset}

To start the platform later, run:
${colors.cyan}npm start${colors.reset}

Then visit:
${colors.cyan}http://localhost:3000${colors.reset} in your browser.
`);
        }
        
        rl.close();
    });
}

// Main function
function main() {
    showWelcome();
    checkNodeVersion();
    checkNpmVersion();
    
    const isReady = checkReadiness();
    
    if (!isReady) {
        installDependencies();
    } else {
        console.log(`
${colors.green}✓ All dependencies are already installed.${colors.reset}
`);
    }
    
    runPlatform();
}

// Run the script
main();
