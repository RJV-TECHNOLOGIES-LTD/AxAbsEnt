#!/bin/bash
echo "🚀 Syncing AxAbsEnt to GitHub..."

cd "$(dirname "$0")/../"

git init
git remote remove origin 2>/dev/null
git remote add origin https://github.com/RJV-TECHNOLOGIES-LTD/AxAbsEnt.git

git add .
git commit -m "🚀 Initial full-system commit of AxAbsEnt recursive AI engine"
git branch -M main
git push -u origin main

echo "✅ Push complete → https://github.com/RJV-TECHNOLOGIES-LTD/AxAbsEnt"
