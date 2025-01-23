#!/bin/bash
# Finish a feature and merge it into dev
feature_name=$1

if [ -z "$feature_name" ]; then
    echo "Please provide a feature name."
    exit 1
fi

git checkout feature/$feature_name
git pull origin feature/$feature_name
git checkout dev
git merge --no-ff feature/$feature_name
git branch -d feature/$feature_name
git push origin dev
echo "Feature $feature_name finished and merged into dev."