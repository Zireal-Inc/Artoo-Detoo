from typing import Optional
from ..base import BaseCommand
from .config import ConfigCommand
import typer
import os
import re

class GitFlowError(Exception):
    pass


class InitCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ConfigCommand(self.gitflow)

    def is_initialized(self) -> bool:
        """Check if repository is initialized for git-flow"""
        main = self.gitflow._git_config_get('gitflow.branch.main')
        develop = self.gitflow._git_config_get('gitflow.branch.develop')
        
        # Check if main and develop branches exist and are different
        if not main or not develop or main == develop:
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
            self.gitflow._git_command(['symbolic-ref', 'HEAD', f'refs/heads/{self.main_branch}'])
            self.gitflow._git_command(['commit', '--allow-empty', '--quiet', '-m', 'Initial commit'])
            return True
        return False

    def sanitize_branch_name(self, name: str) -> str:
        """Sanitize branch name"""
        return re.sub(r'[^a-zA-Z0-9_\-./]', '', name)

    def init(self, defaults: bool = False, force: bool = False) -> None:
        """Initialize git-flow configuration"""
        try:
            # Check if git repository exists
            if not self.gitflow.git_dir:
                raise ValueError("Not a git repository")

            # Check if already initialized
            if not force and self.config.list():
                raise ValueError(f"Git flow is already initialized in this repository {self.gitflow.config_path}")

            # Initialize configuration
            if defaults:
                # Use default configuration
                self.config.init(interactive=False)
            else:
                # Interactive configuration
                self.config.init(interactive=True)

            # Create initial branches if they don't exist
            self._setup_branches()

            typer.echo("Git flow has been initialized successfully")

        except Exception as e:
            raise ValueError(f"Initialization failed: {str(e)}")

    def _setup_branches(self) -> None:
        """Setup initial branches (main and develop)"""
        try:
            # Ensure repo exists and has initial commit
            self.ensure_repo_exists()
            initial_commit_created = self.create_initial_commit()
            
            current_branch = None
            if not initial_commit_created:
                try:
                    current_branch = self.gitflow.get_current_branch()
                except:
                    pass

            # Setup main branch
            try:
                if not self.gitflow.branch_exists(self.gitflow.main_branch):
                    if current_branch:
                        # Create main from current branch
                        self.gitflow._git_command(['branch', self.gitflow.main_branch])
                    else:
                        # Create main and switch to it
                        self.gitflow._git_command(['checkout', '-b', self.gitflow.main_branch])
                else:
                    # Ensure we're on main branch
                    self.gitflow._git_command(['checkout', self.gitflow.main_branch])
            except:
                # If main branch creation fails, create it from current HEAD
                self.gitflow._git_command(['checkout', '-b', self.gitflow.main_branch])

            # Setup develop branch
            if not self.gitflow.branch_exists(self.gitflow.develop_branch):
                # Create develop from main
                self.gitflow._git_command(['checkout', '-b', self.gitflow.develop_branch])
            
            # Return to original branch if possible
            if current_branch and self.gitflow.branch_exists(current_branch):
                self.gitflow._git_command(['checkout', current_branch])
            
        except Exception as e:
            raise ValueError(f"Failed to setup branches: {str(e)}")
