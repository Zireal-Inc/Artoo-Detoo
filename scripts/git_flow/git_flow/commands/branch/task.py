from typing import Optional
from ..base import BaseCommand

class TaskCommand(BaseCommand):
    def start(self, feature_name: str, task_name: str, base: Optional[str] = None):
        """Create a task branch from a feature"""
        feature_branch = f"{self.gitflow.prefix['feature']}{feature_name}"
        task_branch = f"{feature_branch}/task/{task_name}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if not self.gitflow.branch_exists(feature_branch):
            raise ValueError(f"Feature branch {feature_branch} does not exist")
            
        if self.gitflow.branch_exists(task_branch):
            raise ValueError(f"Task branch {task_branch} already exists")
            
        base = base or feature_branch
        self.gitflow.create_branch(task_branch, base)

    def finish(self, feature_name: str, task_name: str):
        """Finish a task branch by merging it back to its feature"""
        feature_branch = f"{self.gitflow.prefix['feature']}{feature_name}"
        task_branch = f"{feature_branch}/task/{task_name}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if not self.gitflow.branch_exists(task_branch):
            raise ValueError(f"Task branch {task_branch} does not exist")
            
        # Switch to feature branch and merge task
        self.gitflow._git_command(['checkout', feature_branch])
        self.gitflow.merge_branch(task_branch)
        self.gitflow.delete_branch(task_branch)
