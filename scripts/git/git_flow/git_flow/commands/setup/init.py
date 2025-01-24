from .base import BaseCommand
import os
import re

class InitCommand(BaseCommand):
    def is_initialized(self) -> bool:
        """Check if repository is initialized for git-flow"""
        master = self.gitflow._git_config_get('gitflow.branch.master')
        develop = self.gitflow._git_config_get('gitflow.branch.develop')
        
        # Check if master and develop branches exist and are different
        if not master or not develop or master == develop:
            return False
            
        # Check if all prefixes are configured
        prefixes = ['feature', 'release', 'hotfix', 'support', 'versiontag']
        for prefix in prefixes:
            if not self.gitflow._git_config_get(f'gitflow.prefix.{prefix}'):
                return False
                
        return True

    def ensure_repo_exists(self):
        """Ensure git repository exists, initialize if needed"""
        if not os.path.exists(os.path.join(self.gitflow.repo_path, '.git')):
            self.gitflow._git_command(['init'])

    def create_initial_commit(self):
        """Create initial commit if repository is empty"""
        try:
            self.gitflow._git_command(['rev-parse', '--verify', 'HEAD'])
        except:
            self.gitflow._git_command(['symbolic-ref', 'HEAD', f'refs/heads/{self.master_branch}'])
            self.gitflow._git_command(['commit', '--allow-empty', '--quiet', '-m', 'Initial commit'])
            return True
        return False

    def sanitize_branch_name(self, name: str) -> str:
        """Sanitize branch name"""
        return re.sub(r'[^a-zA-Z0-9_\-./]', '', name)

    def init(self, defaults: bool = False, force: bool = False):
        """Initialize git-flow in repository"""
        try:
            # Check if already initialized
            if self.is_initialized() and not force:
                print("Already initialized for git-flow.")
                print("To force reinitialization, use force=True")
                return

            # Ensure repository exists
            self.ensure_repo_exists()

            # Get branch counts
            branches = self.gitflow.get_branches()
            branch_count = len(branches)

            # Set master branch
            if not self.gitflow._git_config_get('gitflow.branch.master') or force:
                master = self.sanitize_branch_name('master' if defaults else 
                    input('Branch name for production releases [master]: ') or 'master')
                
                if not self.gitflow.validate_branch_name(master):
                    raise ValueError(f"Invalid master branch name: {master}")
                
                # Check branch existence for existing repos
                if branch_count > 0 and not self.gitflow.branch_exists(master):
                    if self.gitflow.branch_exists(f'origin/{master}'):
                        self.gitflow._git_command(['branch', master, f'origin/{master}'])
                    else:
                        raise ValueError(f"Local branch '{master}' does not exist.")
                        
                self.gitflow._git_config_set('gitflow.branch.master', master)

            # Set develop branch
            if not self.gitflow._git_config_get('gitflow.branch.develop') or force:
                develop = self.sanitize_branch_name('develop' if defaults else 
                    input('Branch name for "next release" development [develop]: ') or 'develop')
                
                if not self.gitflow.validate_branch_name(develop):
                    raise ValueError(f"Invalid develop branch name: {develop}")
                
                if master == develop:
                    raise ValueError("Production and integration branches should differ.")
                    
                # Create develop branch if it doesn't exist
                if not self.gitflow.branch_exists(develop):
                    if self.gitflow.branch_exists(f'origin/{develop}'):
                        self.gitflow._git_command(['branch', develop, f'origin/{develop}'])
                    else:
                        self.gitflow._git_command(['branch', '--no-track', develop, master])
                        
                self.gitflow._git_config_set('gitflow.branch.develop', develop)

            # Create initial commit and HEAD if needed
            created_branches = self.create_initial_commit()

            # Set prefixes
            prefixes = {
                'feature': 'feature/',
                'release': 'release/',
                'hotfix': 'hotfix/',
                'support': 'support/',
                'versiontag': ''
            }

            for name, default in prefixes.items():
                if not self.gitflow._git_config_get(f'gitflow.prefix.{name}'):
                    prefix = default if defaults else input(f'{name} branches? [{default}]: ') or default
                    self.gitflow._git_config_set(f'gitflow.prefix.{name}', prefix)

            # Switch to develop if we created new branches
            if created_branches:
                self.gitflow._git_command(['checkout', '-q', develop])
                
        except Exception as e:
            raise GitFlowError(f"Initialization failed: {str(e)}")
