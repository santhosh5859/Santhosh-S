const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('Starting Vercel deployment...');

// Check if .vercel directory exists
const vercelDir = path.join(__dirname, '.vercel');
if (!fs.existsSync(vercelDir)) {
  console.log('Initializing Vercel project...');
  exec('npx vercel link --yes', { cwd: __dirname }, (error, stdout, stderr) => {
    if (error) {
      console.error('Error initializing Vercel project:', error.message);
      return;
    }
    console.log('Vercel project initialized successfully');
    deploy();
  });
} else {
  deploy();
}

function deploy() {
  console.log('Deploying to Vercel...');
  const vercel = exec('npx vercel --prod', { cwd: __dirname });
  
  vercel.stdout.on('data', (data) => {
    console.log(data.toString());
  });
  
  vercel.stderr.on('data', (data) => {
    console.error(data.toString());
  });
  
  vercel.on('close', (code) => {
    if (code === 0) {
      console.log('Deployment completed successfully!');
    } else {
      console.error(`Deployment failed with code ${code}`);
    }
  });
}
