from typing import Optional, List, Tuple
from ..base import BaseCommand

class SupportCommand(BaseCommand):
    def start(self, version: str, base: str):
        """Start a new support branch
        
        Args:
            version: Version/name for the support branch
            base: Base commit to start from (must be on main)
        """
        branch = f"{self.gitflow.prefix['support']}{version}"
        
        # Sanity checks
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        # Verify base is on main
        master_commits = self.gitflow._git_command(['branch', '--no-color', '--contains', base]).splitlines()
        if not any(b.strip() == self.gitflow.main_branch for b in master_commits):
            raise ValueError(f"Base {base} is not a valid commit on {self.gitflow.main_branch}")
            
        # Create branch
        self.gitflow._git_command(['checkout', '-b', branch, base])
        
    def list(self, verbose: bool = False) -> List[Tuple[str, str, str, bool]]:
        """List all support branches
        
        Args:
            verbose: Show detailed status information

        Returns:
            List of tuples containing (full_name, name, status, is_current)
        """
        support_branches = []
        current = self.gitflow.get_current_branch()
        
        for branch in self.gitflow.get_branches():
            if not branch.startswith(self.gitflow.prefix['support']):
                continue
                
            name = branch[len(self.gitflow.prefix['support']):]
            if verbose:
                base = self.gitflow._git_command(['merge-base', branch, self.gitflow.main_branch]).strip()
                master_sha = self.gitflow._git_command(['rev-parse', self.gitflow.main_branch]).strip()
                branch_sha = self.gitflow._git_command(['rev-parse', branch]).strip()
                
                status = ""
                if branch_sha == master_sha:
                    status = "(no commits yet)"
                else:
                    try:
                        # Try to get tag name
                        tag = self.gitflow._git_command(['name-rev', '--tags', '--no-undefined', '--name-only', base]).strip()
                        status = f"(based on {tag})"
                    except:
                        # Fall back to short SHA
                        short_sha = self.gitflow._git_command(['rev-parse', '--short', base]).strip()
                        status = f"(based on {short_sha})"
                        
                support_branches.append((branch, name, status, branch == current))
            else:
                support_branches.append((branch, name, "", branch == current))
                
        return support_branches
