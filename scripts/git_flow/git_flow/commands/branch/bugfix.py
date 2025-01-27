from ..base import BaseCommand

class BugfixCommand(BaseCommand):
    def __init__(self, gitflow):
        super().__init__(gitflow)
        self.prefix = self.gitflow.prefix['bugfix']

    def start(self, name: str):
        """Start a new bugfix branch"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
        
        bugfix_branch = f"{self.prefix}{name}"
        if self.gitflow.branch_exists(bugfix_branch):
            raise ValueError(f"Bugfix branch '{bugfix_branch}' already exists")
            
        self.gitflow._git_command(['checkout', '-b', bugfix_branch, self.gitflow.develop_branch])
        return bugfix_branch

    def finish(self, name: str):
        """Finish a bugfix branch"""
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        bugfix_branch = f"{self.prefix}{name}"
        if not self.gitflow.branch_exists(bugfix_branch):
            raise ValueError(f"Bugfix branch '{bugfix_branch}' does not exist")
            
        self.gitflow._git_command(['checkout', self.gitflow.develop_branch])
        self.gitflow.merge_branch(bugfix_branch)
        self.gitflow.delete_branch(bugfix_branch)
