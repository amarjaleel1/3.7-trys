#!/bin/bash
echo "Starting AI Learning Platform..."
echo
cd "$(dirname "$0")"
echo "Installing dependencies..."
npm install
echo
echo "Starting server on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo
npm start
