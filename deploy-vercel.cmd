@echo off
echo Creating Vercel deployment...

rem Install Vercel CLI globally if not already installed
npm install -g vercel

rem Build the project
echo Building the project...
npm run build

rem Run Vercel deployment
echo Starting Vercel deployment...
vercel --prod

echo Deployment completed! Check the URL provided above.
pause
