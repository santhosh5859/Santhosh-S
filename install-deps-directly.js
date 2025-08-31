const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Create a temporary package.json if it doesn't exist
const packageJsonPath = path.join(__dirname, 'package.json');
if (!fs.existsSync(packageJsonPath)) {
    fs.writeFileSync(packageJsonPath, JSON.stringify({
        name: 'product-showcase',
        version: '1.0.0',
        private: true,
        dependencies: {}
    }, null, 2));
}

// Install dependencies
console.log('Installing dependencies...');
const command = 'node -e "const {exec} = require(\'child_process\').exec; exec(\'npm install framer-motion @heroicons/react\', (err, stdout, stderr) => { console.log(stdout); if (err) { console.error(\'Error installing dependencies:\', err); process.exit(1); } console.log(\'Dependencies installed successfully!\'); })"';

exec(command, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing command: ${error}`);
        return;
    }
    console.log(stdout);
    console.error(stderr);
});
