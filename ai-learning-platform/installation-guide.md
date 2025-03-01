# AI Learning Platform Installation Guide

Follow these step-by-step instructions to set up and run the AI Learning Platform on your local machine.

## Prerequisites

Before getting started, make sure you have the following installed:

1. **Node.js** (version 14 or later)
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation by running `node -v` in your command prompt or terminal

## Installation Steps

1. **Navigate to the project folder**
   Open your command prompt or terminal and navigate to the project directory:
   ```bash
   cd /d:/3.7 trys/ai-learning-platform
   ```

2. **Install dependencies**
   Run the following command to install all required packages:
   ```bash
   npm install
   ```
   This will install Express.js and other dependencies defined in the package.json file.

3. **Start the server**
   Run the following command to start the local server:
   ```bash
   npm start
   ```

4. **Access the application**
   Open your web browser and visit:
   ```
   http://localhost:3000
   ```

## Troubleshooting

If you encounter any issues:

1. **Port already in use**
   - If port 3000 is already in use, you can change the port in server.js
   - After changing, restart the server

2. **Missing dependencies**
   - If you see errors about missing modules, try running `npm install` again

3. **File permissions**
   - Ensure you have read/write permissions in the project directory

## Development Mode

If you want to automatically restart the server when making code changes:

1. Install nodemon as a dev dependency (if not already installed):
   ```bash
   npm install --save-dev nodemon
   ```

2. Run the server in development mode:
   ```bash
   npm run dev
   ```
