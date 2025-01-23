from typing import Optional
from .base import BaseCommand

class SetupCommand(BaseCommand):
    def start(self, name: str, base: Optional[str] = None):
        """Start a new setup branch"""
        if base is None:
            base = self.gitflow.develop_branch
            
        branch = f"{self.gitflow.prefix.get('setup', 'setup/')}{name}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        # Create and switch to setup branch
        self.gitflow.create_branch(branch, base)
        
    def finish(self, name: str):
        """Finish a setup branch"""
        branch = f"{self.gitflow.prefix.get('setup', 'setup/')}{name}"
        
        if not self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} does not exist")
            
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        # Merge setup branch back to base branch and delete it
        self.gitflow.merge_branch(branch)
        self.gitflow.delete_branch(branch)
        
    def list(self) -> list:
        """List all setup branches"""
        setup_branches = []
        prefix = self.gitflow.prefix.get('setup', 'setup/')
        
        for branch in self.gitflow.get_branches():
            if branch.startswith(prefix):
                name = branch[len(prefix):]
                setup_branches.append(name)
                
        return setup_branches
