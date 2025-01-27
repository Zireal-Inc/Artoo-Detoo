from typing import Optional, List
from ..base import BaseCommand

class FeatureCommand(BaseCommand):
    def start(self, name: str, base: Optional[str] = None):
        """Start a new feature branch"""
        if base is None:
            base = self.gitflow.develop_branch
            
        branch = f"{self.gitflow.prefix['feature']}{name}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        self.gitflow.create_branch(branch, base)
        
    def finish(self, name: str):
        """Finish a feature branch"""
        branch = f"{self.gitflow.prefix['feature']}{name}"
        
        if not self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} does not exist")
            
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        # Switch to develop and merge feature
        self.gitflow.merge_branch(branch)
        self.gitflow.delete_branch(branch)

    def list(self, verbose: bool = False) -> List[str]:
        """List all feature branches"""
        feature_branches = []
        current = self.gitflow.get_current_branch()
        
        for branch in self.gitflow.get_branches():
            if not branch.startswith(self.gitflow.prefix['feature']):
                continue
                
            name = branch[len(self.gitflow.prefix['feature']):]
            if verbose:
                base = self.gitflow._git_command(['merge-base', branch, self.gitflow.develop_branch]).strip()
                develop_sha = self.gitflow._git_command(['rev-parse', self.gitflow.develop_branch]).strip()
                branch_sha = self.gitflow._git_command(['rev-parse', branch]).strip()
                
                status = ""
                if branch_sha == develop_sha:
                    status = "(no commits yet)"
                elif base == branch_sha:
                    status = "(is behind develop, may ff)"
                elif base == develop_sha:
                    status = "(based on latest develop)"
                else:
                    status = "(may be rebased)"
                    
                feature_branches.append((branch, name, status, branch == current))
            else:
                feature_branches.append((branch, name, "", branch == current))
                
        return feature_branches

    def publish(self, name: str):
        """Publish feature branch to remote"""
        branch = f"{self.gitflow.prefix['feature']}{name}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if not self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} does not exist")
            
        # Check if remote branch exists
        if self.gitflow.branch_exists(f"{self.gitflow.origin}/{branch}"):
            raise ValueError(f"Remote branch {branch} already exists")
            
        # Push to remote and set up tracking
        self.gitflow._git_command(['push', self.gitflow.origin, f"{branch}:refs/heads/{branch}"])
        self.gitflow._git_command(['config', f"branch.{branch}.remote", self.gitflow.origin])
        self.gitflow._git_command(['config', f"branch.{branch}.merge", f"refs/heads/{branch}"])

    def track(self, name: str):
        """Track remote feature branch"""
        branch = f"{self.gitflow.prefix['feature']}{name}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        if not self.gitflow.branch_exists(f"{self.gitflow.origin}/{branch}"):
            raise ValueError(f"Remote branch {branch} does not exist")
            
        self.gitflow._git_command(['checkout', '-b', branch, f"{self.gitflow.origin}/{branch}"])

    def diff(self, name: Optional[str] = None):
        """Show diff of feature branch"""
        if name:
            branch = f"{self.gitflow.prefix['feature']}{name}"
            if not self.gitflow.branch_exists(branch):
                raise ValueError(f"Branch {branch} does not exist")
        else:
            current = self.gitflow.get_current_branch()
            if not current.startswith(self.gitflow.prefix['feature']):
                raise ValueError("Not on a feature branch")
            branch = current
            
        base = self.gitflow._git_command(['merge-base', self.gitflow.develop_branch, branch]).strip()
        return self.gitflow._git_command(['diff', f"{base}..{branch}"])

    def rebase(self, name: Optional[str] = None, interactive: bool = False):
        """Rebase feature branch on develop"""
        if name:
            branch = f"{self.gitflow.prefix['feature']}{name}"
            if not self.gitflow.branch_exists(branch):
                raise ValueError(f"Branch {branch} does not exist")
        else:
            current = self.gitflow.get_current_branch()
            if not current.startswith(self.gitflow.prefix['feature']): 
                raise ValueError("Not on a feature branch")
            branch = current
            
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        args = ['rebase']
        if interactive:
            args.append('-i')
        args.append(self.gitflow.develop_branch)
        
        self.gitflow._git_command(['checkout', branch])
        self.gitflow._git_command(args)

    def pull(self, remote: str, name: Optional[str] = None, rebase: bool = False):
        """Pull feature branch from remote"""
        if name:
            branch = f"{self.gitflow.prefix['feature']}{name}"
        else:
            current = self.gitflow.get_current_branch()
            if not current.startswith(self.gitflow.prefix['feature']):
                raise ValueError("Not on a feature branch")
            branch = current
            
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        # Create branch if it doesn't exist
        if not self.gitflow.branch_exists(branch):
            self.gitflow._git_command(['fetch', remote, branch])
            self.gitflow._git_command(['branch', '--no-track', branch, 'FETCH_HEAD'])
            self.gitflow._git_command(['checkout', branch])
        else:
            # Pull changes
            args = ['pull']
            if rebase:
                args.append('--rebase')
            args.extend([remote, branch])
            self.gitflow._git_command(args)
