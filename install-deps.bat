@echo off
echo Installing required dependencies...

:: Create a temporary package.json if it doesn't exist
if not exist package.json (
    echo Creating package.json...
    echo {^"name": "product-showcase", "version": "1.0.0", "private": true, "dependencies": {^}} > package.json
)

:: Install dependencies
node -e "const fs = require('fs'); const packageJson = JSON.parse(fs.readFileSync('package.json')); if (!packageJson.dependencies) packageJson.dependencies = {}; if (!packageJson.dependencies['framer-motion']) { console.log('Installing framer-motion...'); const { execSync } = require('child_process'); execSync('npm install framer-motion --save', { stdio: 'inherit' }); }"

node -e "const fs = require('fs'); const packageJson = JSON.parse(fs.readFileSync('package.json')); if (!packageJson.dependencies) packageJson.dependencies = {}; if (!packageJson.dependencies['@heroicons/react']) { console.log('Installing @heroicons/react...'); const { execSync } = require('child_process'); execSync('npm install @heroicons/react --save', { stdio: 'inherit' }); }"

echo.
echo Dependencies installed successfully!
pause
