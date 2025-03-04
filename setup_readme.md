# Project Setup 

This document outlines the steps required to set up the development environment. 
Before starting, ensure you have Node.js (latest LTS) installed on your system.

## TOC []

## Git Setup 

Git is a distributed version control system that allows you to track changes to your codebase. It enables collaboration, facilitates experimentation, and simplifies the process of reverting to previous states.

### 1. Git Initiate

```sh
git init 
git checkout -b setup-workspace
git add .
git commit -am 'Initial Commit'
```

- `git init`: Initializes a new Git repository.
- `git checkout -b setup-workspace`: Creates and switches to a new branch named `setup-workspace`.
- `git add .`: Stages all changes in the current directory for the next commit.
- `git commit -am 'Initial Commit'`: Commits the staged changes with the message 'Initial Commit'.

## Package Manager Setup

will be PNPM as package manager 

### 0. Install PNPM 

```sh
npm -g pnpm@latest
```
This step ensures that you have the latest version of PNPM installed globally. 
PNPM reduces disk space usage by linking packages from a shared store.

### 1 . PNPM INIT

check if step 0 is required or not 
```sh
pnpm init
```
This command initializes a new PNPM project.

### 2. Create the Following dir with readme.md files 

```sh
mkdir apps && cd apps && echo "# apps" > README.md && cd ..
mkdir libs && cd libs && echo "# libs" > README.md && cd ..
mkdir tools && cd tools && echo "# tools" > README.md && cd ..
mkdir configs && cd configs && echo "# configs" > README.md && cd ..
mkdir scripts && cd scripts && echo "# scripts" > README.md && cd ..
mkdir features && cd features && echo "# features" > README.md && cd ..
mkdir packages && cd packages && echo "# packages" > README.md && cd ..
```

### 3. Setup PNPM workspace 

```sh 
code pnpm-workspace.yaml
```

```yaml
packages:
    # executable/launch-able applications
    - 'apps/*'
    # all packages in sub dirs of packages/ and components/
    - 'packages/*'
    # all the configs in the config
    - 'configs/*'
```

#### 4. Add PNPM as dev dependency 

```sh
pnpm add -D pnpm
```


## Nx Setup 

```sh 
pnpm add -D nx
pnpm dlx nx@latest init --nxCloud=false

```
## Workspace Setup

steps

 1. [Git Setup](#git-setup): Initializes a Git repository, creates a dedicated branch, and commits initial changes.
 2. [PNPM Setup](#package-manager-setup): Prepares the project for installing and managing dependencies with PNPM. Use this to create a package.json file.

> For best results, confirm your Node.js version supports PNPM and that all required system dependencies are installed.
 
 3. [Nx Setup](#nx-setup) :
 4.
