@echo off
echo Running TypeScript type checking...

:: Use the local TypeScript binary
node_modules\.bin\tsc --noEmit

if %ERRORLEVEL% EQU 0 (
    echo Type checking completed successfully!
) else (
    echo Type checking found errors. Please fix the issues above.
)

exit /b %ERRORLEVEL%
