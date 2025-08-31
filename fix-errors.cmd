@echo off
echo Fixing common TypeScript and linting issues...

:: Create a temporary tsconfig.json with stricter settings
echo Creating temporary tsconfig.json...
(
echo {
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
) > tsconfig.temp.json

echo Running TypeScript type checking...
npx tsc --project tsconfig.temp.json --noEmit

echo.
echo If you see TypeScript errors, please fix them in your source files.
echo Common fixes include:
echo 1. Adding proper type annotations
echo 2. Adding null/undefined checks
echo 3. Fixing module imports
echo 4. Installing missing @types packages
echo.

del /f tsconfig.temp.json

echo Running ESLint to find and fix issues...
npx eslint . --ext .js,.jsx,.ts,.tsx --fix

echo.
echo If you see ESLint errors, please fix them in your source files.
echo Common fixes include:
echo 1. Adding missing dependencies to the import statements
echo 2. Fixing code style issues
echo 3. Adding proper TypeScript types
echo.

echo Done! Review the output above for any remaining issues.
