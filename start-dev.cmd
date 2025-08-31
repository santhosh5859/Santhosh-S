@echo off
set NODE_OPTIONS=--openssl-legacy-provider
set NODE_ENV=development
set PORT=3000

echo Starting development server...
echo.
echo If you see any errors about missing dependencies, please run 'install-deps.cmd' first.
echo.

npm run dev
