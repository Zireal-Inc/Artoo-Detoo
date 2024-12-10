#!/bin/bash
# Finish a hotfix and merge it into master and dev 
hotfix_name=$1 

if [ -z "$hotfix_name" ]; then 
    echo "Please provide a hotfix name." 
    exit 1 
fi 

git checkout hotfix/$hotfix_name 
git pull origin hotfix/$hotfix_name 

# Merge into master 
git checkout master 
git merge --no-ff hotfix/$hotfix_name 

# Merge back into dev to keep it updated 
git checkout dev 
git merge --no-ff hotfix/$hotfix_name 

# Clean up the hotfix branch 
git branch -d hotfix/$hotfix_name 

# Push changes to remote repository 
git push origin master 
git push origin dev 
echo "Hotfix $hotfix_name finished and merged into master and dev."