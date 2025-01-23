#!/bin/bash
# Finish a release and merge it into master and dev
release_version=$1

if [ -z "$release_version" ]; then
    echo "Please provide a release version."
    exit 1
fi

git checkout release/$release_version
git pull origin release/$release_version

# Merge into master and tag the release
git checkout master
git merge --no-ff release/$release_version
git tag -a $release_version -m "Release $release_version"

# Merge back into dev to keep it updated
git checkout dev
git merge --no-ff release/$release_version

# Clean up the release branch
git branch -d release/$release_version

# Push changes to remote repository including tags
git push origin master --tags 
git push origin dev 
echo "Release $release_version finished and merged into master and dev."