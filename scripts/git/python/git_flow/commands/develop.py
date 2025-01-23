from typing import Optional, List
from .base import BaseCommand

class DevelopCommand(BaseCommand):
    def checkout(self):
        """Checkout develop branch"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['checkout', self.gitflow.develop_branch])
        
    def pull(self, rebase: bool = False):
        """Pull latest changes from remote develop"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        args = ['pull']
        if rebase:
            args.append('--rebase')
        args.extend([self.gitflow.origin, self.gitflow.develop_branch])
        
        self.gitflow._git_command(args)
        
    def push(self):
        """Push changes to remote develop"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['push', self.gitflow.origin, self.gitflow.develop_branch])
            
    def merge(self, branch: str, no_ff: bool = True):
        """Merge branch into develop"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['checkout', self.gitflow.develop_branch])
        self.gitflow.merge_branch(branch, no_ff=no_ff)
        
    def sync(self):
        """Sync develop with master"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['checkout', self.gitflow.develop_branch])
        self.gitflow.merge_branch(self.gitflow.master_branch, no_ff=True)

    def start(self, name: str, base: Optional[str] = None):
        raise NotImplementedError("Develop branch does not support start")
        
    def finish(self, name: str):
        raise NotImplementedError("Develop branch does not support finish")
        
    def list(self):
        raise NotImplementedError("Develop branch does not support list")
        
    def publish(self, name: str):
        raise NotImplementedError("Develop branch does not support publish")
