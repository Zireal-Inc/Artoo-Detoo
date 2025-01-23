#!/bin/bash
# Start a new release
release_version=$1

if [ -z "$release_version" ]; then
    echo "Please provide a release version."
    exit 1
fi

git checkout dev
git pull origin dev
git checkout -b release/$release_version
echo "Started release branch: release/$release_version"