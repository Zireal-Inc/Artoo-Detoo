# Nx - Mono Repo Setup

## Node Setup

```bash
#update the all the lib list
sudo apt-get update
#updgrade the os if required 
sudo apt-get updgrade 
#install Node 
sudo apt-get install nodejs
#update node 
npm install 22 # 22 LTs or any version 
```

## PNPM Setup

```sh
#intall PNPM package manager 
npm install -g pnpm
```

* create .npmrc to avoid PNPM to install dependency in the workspace instead of globally
```ini
ignore-workspace-root-check=true 
```

```sh
#create package.json 
pnpm init
```

* create pnpm-workspace.yaml
```yaml
packages:
    # executable/launchable applications
  - 'apps/*'
    # all packages in subdirs of packages/ and components/
  - 'packages/*'
    # all the cofign in the config
  - 'configs/*'
```

```sh 
echo "creating pnpm-workspace.yaml dir"
mkdir apps
mkdir packages
mkdir configs
```

## Nx Setup

```sh 
# add nx as PNPM package dev dependency 
pnpm add -D nx@latest
```