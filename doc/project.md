# Project Documentation

## Overview

This project is a monorepo managed using Nx and PNPM. It includes multiple applications and libraries, with comprehensive tooling and configuration for development and collaboration.

## Project Structure

The workspace is organized into the following directories:

- `.github/`: Contains GitHub configuration files, issue templates, pull request templates, and other GitHub-related configurations.
- `.nx/`: Contains Nx workspace data and cache.
- `.vscode/`: Contains VS Code settings.
- `apps/`: Contains application projects.
  - `web/`: Placeholder for web applications.
  - `www/`: Placeholder for other web applications.
- `configs/`: Contains configuration files.
- `doc/`: Contains documentation files. 
- `packages/`: Contains library projects.
  - `test/`: Placeholder for test libraries.
  - `ui/`: Contains the UI library.
- `scripts/`: Contains various scripts for setting up and managing the monorepo.

## Tooling and Configuration

### Nx

Nx is used for managing the monorepo. It provides powerful tools for building, testing, and managing projects within the workspace.

### PNPM

PNPM is used as the package manager. It is configured to manage dependencies and workspaces efficiently.

### ESLint

ESLint is configured for linting the codebase. It ensures code quality and consistency across the projects.

### Cypress

Cypress is used for end-to-end testing. It is configured to run tests and ensure the applications work as expected.

### Vite

Vite is used as the build tool for the applications. It provides fast and efficient builds.

## Setting Up the Project

### Node Setup

```bash
# Update the package list
sudo apt-get update
# Upgrade the OS if required
sudo apt-get upgrade
# Install Node.js
sudo apt-get install nodejs
# Update Node.js
npm install 22 # 22 LTS or any version
```

### PNPM Setup

```sh
# Install PNPM package manager
npm install -g pnpm
```

Create `.npmrc` to avoid PNPM installing dependencies in the workspace instead of globally:

```ini
ignore-workspace-root-check=true
```

Initialize the PNPM workspace:

```sh
# Create package.json
pnpm init
```

Create `pnpm-workspace.yaml`:

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'configs/*'
```

Create directories:

```sh
mkdir apps
mkdir packages
mkdir configs
```

### Nx Setup

```sh
# Add Nx as a PNPM package dev dependency
pnpm add -D nx@latest
```

Create an Nx application:

```sh
nx add @nx/react
pnpm add -D @nx/react
```

## Running the Project

### Building the Project

To build the project, run the following command:

```sh
pnpm run build
```

### Running Tests

To run the tests, use the following command:

```sh
pnpm run test
```

### Linting the Code

To lint the code, use the following command:

```sh
pnpm run lint
```

## Contributing

Please read the [CONTRIBUTING.md](../.github/CONTRIBUTING.md) file for details on the process for submitting pull requests and issue reports.

## Code of Conduct

Please read the [CODE_OF_CONDUCT.md](../.github/CODE_OF_CONDUCT.md) file for details on our code of conduct.

## Security

Please read the [SECURITY.md](../.github/SECURITY.md) file for details on how to report security issues.

## Support

Please read the [SUPPORT.md](../.github/SUPPORT.md) file for details on how to obtain support.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
