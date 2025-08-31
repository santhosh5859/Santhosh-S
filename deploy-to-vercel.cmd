@echo off
echo Starting Vercel deployment...

:: Check if Vercel CLI is installed
vercel -v >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Vercel CLI not found. Installing Vercel CLI...
    npm install -g vercel
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Vercel CLI. Please install it manually: npm install -g vercel
        pause
        exit /b 1
    )
)

echo Building the application...
call npm run build
if %ERRORLEVEL% neq 0 (
    echo Build failed. Please fix the errors and try again.
    pause
    exit /b 1
)

echo Deploying to Vercel...
vercel --prod

if %ERRORLEVEL% neq 0 (
    echo Deployment failed. Please check the error messages above.
    pause
    exit /b 1
)

echo Deployment completed successfully!
pause
