@echo off
echo Installing required dependencies...

:: Install main dependencies
npm install next@13.4.7 react@18.2.0 react-dom@18.2.0

:: Install TypeScript and type definitions
npm install --save-dev typescript@5.1.6 @types/react@18.2.14 @types/node@20.4.1 @types/react-dom@18.2.6

:: Install other dependencies
npm install framer-motion@10.12.18 @heroicons/react@2.0.18

:: Install development dependencies
npm install --save-dev autoprefixer@10.4.14 postcss@8.4.25 tailwindcss@3.3.2 eslint@8.44.0 eslint-config-next@13.4.7

echo Installation complete! Run 'npm run dev' to start the development server.
