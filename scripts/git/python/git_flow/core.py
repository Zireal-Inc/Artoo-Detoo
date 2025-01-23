import os
import subprocess
import re
from typing import List, Optional, Tuple
from .settings import Settings

class GitFlow:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = os.path.abspath(repo_path)
        self.git_dir = self._get_git_dir()
        self.config_path = os.path.join(self.repo_path, 'git_flow', 'config.toml')
        self.settings = Settings(self.config_path)
        self._load_settings()

    def _get_git_dir(self) -> str:
        """Get .git directory path"""
        result = self._git_command(['rev-parse', '--git-dir'])
        return os.path.abspath(result.strip())

    def _load_settings(self):
        """Load settings from config file"""
        config = self.settings.read_config()
        branch_config = config.get('branch', {})
        
        self.master_branch = branch_config.get('main', {}).get('default', 'main')
        self.develop_branch = branch_config.get('develop', {}).get('default', 'develop')
        self.origin = config.get('remote', {}).get('default', 'origin')
        
        self.prefix = {}
        for branch_type in ['feature', 'release', 'hotfix', 'support', 'bugfix', 'version']:
            self.prefix[branch_type] = branch_config.get(branch_type, {}).get('prefix', '')

    def _git_command(self, args: List[str], check: bool = True) -> str:
        """Execute git command and return output"""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise GitFlowError(f"Git command failed: {e.stderr}")

    def _git_config_get(self, key: str) -> Optional[str]:
        """Get git config value"""
        try:
            return self._git_command(['config', '--get', key]).strip()
        except GitFlowError:
            return None

    def _git_config_set(self, key: str, value: str):
        """Set git config value"""
        self._git_command(['config', key, value])

    def get_current_branch(self) -> str:
        """Get current branch name"""
        result = self._git_command(['branch', '--show-current'])
        return result.strip()

    def is_clean_working_tree(self) -> bool:
        """Check if working tree is clean"""
        try:
            self._git_command(['diff', '--no-ext-diff', '--quiet'])
            self._git_command(['diff-index', '--cached', '--quiet', 'HEAD', '--'])
            return True
        except GitFlowError:
            return False

    def branch_exists(self, branch: str) -> bool:
        """Check if branch exists"""
        try:
            self._git_command(['rev-parse', '--verify', branch], check=False)
            return True
        except GitFlowError:
            return False

    def get_branches(self, remote: bool = False) -> List[str]:
        """Get list of branches"""
        args = ['branch', '--no-color']
        if remote:
            args.append('-r')
        result = self._git_command(args)
        return [b.strip() for b in result.splitlines()]

    def create_branch(self, branch: str, base: str):
        """Create new branch"""
        self._git_command(['checkout', '-b', branch, base])

    def merge_branch(self, branch: str, no_ff: bool = True):
        """Merge branch"""
        args = ['merge']
        if no_ff:
            args.append('--no-ff')
        args.append(branch)
        self._git_command(args)

    def delete_branch(self, branch: str, force: bool = False):
        """Delete branch"""
        args = ['branch']
        if force:
            args.append('-D')
        else:
            args.append('-d')
        args.append(branch)
        self._git_command(args)

    def get_remote_branches(self) -> List[str]:
        """Get list of remote branches"""
        return [b.strip() for b in self._git_command(['branch', '-r', '--no-color']).splitlines()]

    def get_all_branches(self) -> List[str]:
        """Get list of all branches (local and remote)"""
        local = self.get_branches()
        remote = self.get_remote_branches()
        return local + remote

    def get_all_tags(self) -> List[str]:
        """Get list of all tags"""
        return self._git_command(['tag']).splitlines()

    def is_headless(self) -> bool:
        """Check if repository is headless"""
        try:
            self._git_command(['rev-parse', '--quiet', '--verify', 'HEAD'])
            return False
        except GitFlowError:
            return True

    def compare_branches(self, branch1: str, branch2: str) -> int:
        """Compare two branches and return their relationship
        Returns:
        0 - Branches point to same commit
        1 - First branch needs fast-forwarding
        2 - Second branch needs fast-forwarding
        3 - Branches need merging
        4 - No merge base (no common ancestors)
        """
        commit1 = self._git_command(['rev-parse', branch1]).strip()
        commit2 = self._git_command(['rev-parse', branch2]).strip()
        
        if commit1 == commit2:
            return 0
            
        try:
            base = self._git_command(['merge-base', commit1, commit2]).strip()
            if commit1 == base:
                return 1
            elif commit2 == base:
                return 2
            else:
                return 3
        except GitFlowError:
            return 4

    def is_branch_merged_into(self, subject: str, base: str) -> bool:
        """Check if subject branch is merged into base branch"""
        try:
            merges = self._git_command(['branch', '--no-color', '--contains', subject])
            merged_branches = [b.strip() for b in merges.splitlines()]
            return base in merged_branches
        except GitFlowError:
            return False

class GitFlowError(Exception):
    pass
