#!/bin/bash
# Start a new feature
feature_name=$1

if [ -z "$feature_name" ]; then
    echo "Please provide a feature name."
    exit 1
fi

git checkout dev
git pull origin dev
git checkout -b feature/$feature_name
echo "Started feature branch: feature/$feature_name"