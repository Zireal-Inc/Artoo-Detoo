#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Function to install or update Node.js
setup_node() {
    # get the latest apt-get list
    sudo apt-get update
    if
        ! command -v node >/dev/null 2>&1
    then
        echo "Node.js is not installed. Installing Node.js..."
        sudo apt-get install -y nodejs
    else
        echo "Node.js is installed. Updating Node.js..."
        sudo npm install -g n
        sudo n latest
    fi
    echo "Node.js setup complete."
}

# Function to install or update npm
setup_npm() {
    echo "Checking for npm..."
    if ! command -v npm >/dev/null 2>&1; then
        echo "npm is not installed. Installing npm..."
        setup_node
    else
        echo "npm is installed. Updating npm..."
        npm install -g npm@latest
    fi
    echo "npm setup complete."
}

# Function to install or update pnpm
setup_pnpm() {
    echo "Checking for pnpm..."
    if ! command -v pnpm >/dev/null; then
        echo "pnpm is not installed. Installing pnpm..."
        npm install -g pnpm
    else
        echo "pnpm is installed. Updating pnpm..."
        npm update -g pnpm
    fi
    echo "pnpm setup complete."
}
# Function to Create NPM Registry
create_npmrc() {
    cat <<EOF >.npmrc
ignore-workspace-root-check=true 
EOF
}
# Function to initialize a PNPM workspace
initialize_pnpm_workspace() {
    workspace_dir="$1"
    echo "Creating PNPM workspace in '$workspace_dir'..."
    mkdir -p "$workspace_dir"
    cd "$workspace_dir"
    create_npmrc
    pnpm init

    # Create the pnpm-workspace.yaml file
    cat <<EOF >pnpm-workspace.yaml
packages:
    # executable/launchable applications
    - 'apps/*'
    # all packages in subdirs of packages/ and components/
    - 'packages/*'
    # all the cofign in the config
    - 'configs/*'
EOF

    #Create All the above package dir
    echo "creating pnpm-workspace.yaml dir"
    mkdir apps
    mkdir packages
    mkdir config
    echo "PNPM workspace initialized in '$workspace_dir'."
}

# Function to setup Nx in the workspace
setup_nx() {
    echo "Setting up Nx in the workspace..."
    pnpm add -D nx
    pnpm dlx nx@latest init --nxCloud=false
    echo "Nx setup complete."
}

# Function to create an Nx application
create_nx_app() {
    app_name="$1"
    echo "Creating Nx application '$app_name'..."
    npx nx generate @nx/react:application "$app_name"

    npx nx generate @nx/react:application apps/app1 --directory=apps --name=app1 --bundler=vite --compiler=swc --style=css --unitTestRunner=vitest --routing=true

    echo "Application '$app_name' created."
}

# Function to create an Nx library
create_nx_library() {
    library_name="$1"
    echo "Creating Nx library '$library_name'..."
    npx nx generate @nx/react:library "$library_name"
    echo "Library '$library_name' created."
}

######################################
#              MAIN                  #
######################################

# Main script execution
main() {
    # Set up the required tools
    setup_npm
    setup_pnpm

    # Initialize workspace
    workspace_dir=$(pwd)
    echo workspace_dir
    initialize_pnpm_workspace "$workspace_dir"

    # Navigate to the workspace
    cd "$workspace_dir"

    # Set up Nx in the workspace
    setup_nx

    echo "Setup complete! Navigate to '$workspace_dir' to start working on your Nx monorepo."
}

# Execute the main function
main
