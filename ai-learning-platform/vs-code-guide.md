# VS Code Setup and Running Guide

This guide explains how to open, run, and develop the AI Learning Platform using Visual Studio Code.

## Prerequisites

Make sure you have the following installed:

1. **Visual Studio Code** - [Download here](https://code.visualstudio.com/)
2. **Node.js** - [Download here](https://nodejs.org/)

## Opening the Project in VS Code

1. **Launch VS Code**

2. **Open the project folder**
   - Click on `File > Open Folder...`
   - Navigate to `/d:/3.7 trys/ai-learning-platform`
   - Click "Select Folder"

3. **Explore the project structure**
   - The Explorer sidebar (left side) will show all project files
   - You can expand folders to see their contents

## Installing Extensions (Recommended)

For a better development experience, install these VS Code extensions:

1. **Live Server** - For quick static page testing
   - Click the Extensions icon in the sidebar (or press `Ctrl+Shift+X`)
   - Search for "Live Server"
   - Click "Install" on the extension by Ritwick Dey

2. **ESLint** - For JavaScript code quality
   - Search for "ESLint" in Extensions
   - Click "Install"

3. **Debugger for JavaScript**
   - Search for "JavaScript Debugger"
   - Click "Install"

## Running the Server From VS Code

### Using the Integrated Terminal

1. **Open the integrated terminal**
   - Press `` Ctrl+` `` (backtick) or select `View > Terminal`
   - A terminal will open at the bottom of VS Code

2. **Install dependencies** (first time only)
   ```bash
   npm install
   ```

3. **Start the server**
   ```bash
   npm start
   ```

4. **Access the application**
   - Open your browser and navigate to [http://localhost:3000](http://localhost:3000)

### Using NPM Scripts

VS Code provides a nice interface for running npm scripts:

1. **Open the NPM Scripts panel**
   - Click on the "Explorer" icon in the sidebar
   - Find and expand "NPM SCRIPTS" at the bottom of the Explorer

2. **Run scripts**
   - You'll see "start" and "dev" scripts listed
   - Click the play button next to "start" to run the server
   - Or click the play button next to "dev" for development mode with auto-restart

## Debugging in VS Code

1. **Set up debug configuration**
   - Go to the Run and Debug view (click the bug icon in the sidebar)
   - Click "create a launch.json file" and select "Node.js"

2. **Add this configuration to the created launch.json file**:
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "type": "node",
               "request": "launch",
               "name": "Launch Server",
               "skipFiles": ["<node_internals>/**"],
               "program": "${workspaceFolder}/server.js"
           }
       ]
   }
   ```

3. **Start debugging**
   - Set breakpoints by clicking in the margin next to the line numbers
   - Press F5 or click the green play button to start debugging
   - The server will start and stop at your breakpoints

## Live Editing Frontend Files

For a more dynamic development experience with the frontend files:

1. **Use Live Server for static development**
   - Right-click on `index.html` in the Explorer
   - Select "Open with Live Server"
   - This will launch the page with auto-refresh on file changes

2. **Or use the Express server with nodemon**
   - Run `npm run dev` in the terminal
   - This starts the server with nodemon, which restarts when files change

## VS Code Shortcuts for Productivity

- `Ctrl+P` - Quick file open
- `Ctrl+Shift+F` - Search across all files
- `Alt+Shift+F` - Format document
- `F5` - Start debugging
- `Ctrl+Shift+`\` - New terminal
- `Ctrl+/` - Toggle comment

## Project Structure in VS Code

The VS Code file explorer makes it easy to understand the project structure:

- `index.html` - Main HTML file
- `css/` - Stylesheet files
- `js/` - JavaScript files for frontend
- `server.js` - Express server code
- `package.json` - Project dependencies and scripts
