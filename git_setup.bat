@echo off
echo Setting up Git repository for Pet Adoption Platform...
echo.

echo Step 1: Initialize Git repository
git init

echo Step 2: Add remote repository
git remote add origin https://github.com/Mekala689/pet-adorption-platform.git

echo Step 3: Add all files
git add .

echo Step 4: Create initial commit
git commit -m "Initial commit: Complete Pet Adoption Platform with Django backend, notifications, and adoption requests"

echo Step 5: Push to GitHub
git branch -M main
git push -u origin main

echo.
echo Repository setup complete!
pause
