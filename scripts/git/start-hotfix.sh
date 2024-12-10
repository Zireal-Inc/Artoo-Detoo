#!/bin/bash
# Start a hotfix for production issues
hotfix_name=$1

if [ -z "$hotfix_name" ]; then
    echo "Please provide a hotfix name."
    exit 1
fi

git checkout main 
git pull origin main 
git checkout -b hotfix/$hotfix_name 
echo "Started hotfix branch: hotfix/$hotfix_name"