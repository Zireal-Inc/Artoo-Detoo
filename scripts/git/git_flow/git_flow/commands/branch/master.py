from typing import Optional, List
from .base import BaseCommand

class MasterCommand(BaseCommand):
    def checkout(self):
        """Checkout master branch"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['checkout', self.gitflow.master_branch])
        
    def pull(self, rebase: bool = False):
        """Pull latest changes from remote master"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        args = ['pull']
        if rebase:
            args.append('--rebase')
        args.extend([self.gitflow.origin, self.gitflow.master_branch])
        
        self.gitflow._git_command(args)
        
    def push(self, tags: bool = False):
        """Push changes to remote master"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['push', self.gitflow.origin, self.gitflow.master_branch])
        if tags:
            self.gitflow._git_command(['push', '--tags', self.gitflow.origin])
            
    def merge(self, branch: str, no_ff: bool = True):
        """Merge branch into master"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        self.gitflow._git_command(['checkout', self.gitflow.master_branch])
        self.gitflow.merge_branch(branch, no_ff=no_ff)

    def start(self, name: str, base: Optional[str] = None):
        raise NotImplementedError("Master branch does not support start")
        
    def finish(self, name: str):
        raise NotImplementedError("Master branch does not support finish")
        
    def list(self):
        raise NotImplementedError("Master branch does not support list")
        
    def publish(self, name: str):
        raise NotImplementedError("Master branch does not support publish")
