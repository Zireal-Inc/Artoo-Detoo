from typing import Optional, List
from ..base import BaseCommand

class HotfixCommand(BaseCommand):
    def start(self, version: str, base: Optional[str] = None):
        """Start a new hotfix branch"""
        if base is None:
            base = self.gitflow.main_branch
            
        branch = f"{self.gitflow.prefix['hotfix']}{version}"
        version_tag = f"{self.gitflow.prefix['version']}{version}"
        
        # Sanity checks
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        # Check if version tag already exists
        if version_tag in self.gitflow.get_all_tags():
            raise ValueError(f"Tag {version_tag} already exists")
            
        # Check if base is on main
        if not self.gitflow._git_command(['branch', '--contains', base]).strip().split('\n')[0].endswith(self.gitflow.main_branch):
            raise ValueError(f"Base {base} is not a valid commit on {self.gitflow.main_branch}")
            
        # Check for existing hotfix branches
        for existing in self.gitflow.get_branches():
            if existing.startswith(self.gitflow.prefix['hotfix']):
                raise ValueError(f"There is an existing hotfix branch ({existing}). Finish that one first.")
                
        self.gitflow.create_branch(branch, base)
        
    def finish(self, version: str, tag_message: Optional[str] = None, sign: bool = False, 
              push: bool = False, keep: bool = False, no_tag: bool = False):
        """Finish a hotfix branch"""
        branch = f"{self.gitflow.prefix['hotfix']}{version}"
        version_tag = f"{self.gitflow.prefix['version']}{version}"
        
        if not self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} does not exist")
            
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        # Try to merge into main
        if not self.gitflow.is_branch_merged_into(branch, self.gitflow.main_branch):
            self.gitflow._git_command(['checkout', self.gitflow.main_branch])
            self.gitflow.merge_branch(branch)
            
        # Create tag if requested
        if not no_tag:
            tag_args = ['tag', '-a']
            if sign:
                tag_args.append('-s')
            if tag_message:
                tag_args.extend(['-m', tag_message])
            tag_args.extend([version_tag, branch])
            self.gitflow._git_command(tag_args)
            
        # Try to merge into develop
        if not self.gitflow.is_branch_merged_into(branch, self.gitflow.develop_branch):
            self.gitflow._git_command(['checkout', self.gitflow.develop_branch])
            self.gitflow.merge_branch(branch)
            
        # Delete branch if not keeping
        if not keep:
            self.gitflow.delete_branch(branch)
            
        # Push if requested
        if push:
            self.gitflow._git_command(['push', self.gitflow.origin, self.gitflow.develop_branch])
            self.gitflow._git_command(['push', self.gitflow.origin, self.gitflow.main_branch])
            if not no_tag:
                self.gitflow._git_command(['push', '--tags', self.gitflow.origin])

    def list(self, verbose: bool = False) -> List[tuple]:
        """List all hotfix branches"""
        hotfix_branches = []
        current = self.gitflow.get_current_branch()
        
        for branch in self.gitflow.get_branches():
            if not branch.startswith(self.gitflow.prefix['hotfix']):
                continue
                
            name = branch[len(self.gitflow.prefix['hotfix']):]
            if verbose:
                base = self.gitflow._git_command(['merge-base', branch, self.gitflow.main_branch]).strip()
                master_sha = self.gitflow._git_command(['rev-parse', self.gitflow.main_branch]).strip()
                branch_sha = self.gitflow._git_command(['rev-parse', branch]).strip()
                
                status = ""
                if branch_sha == master_sha:
                    status = "(no commits yet)"
                else:
                    try:
                        tagname = self.gitflow._git_command(['name-rev', '--tags', '--no-undefined', '--name-only', base]).strip()
                        status = f"(based on {tagname})"
                    except:
                        short_sha = self.gitflow._git_command(['rev-parse', '--short', base]).strip()
                        status = f"(based on {short_sha})"
                        
                hotfix_branches.append((branch, name, status, branch == current))
            else:
                hotfix_branches.append((branch, name, "", branch == current))
                
        return hotfix_branches

    def publish(self, version: str):
        """Publish hotfix branch to remote"""
        branch = f"{self.gitflow.prefix['hotfix']}{version}"
        
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

    def track(self, version: str):
        """Track remote hotfix branch"""
        branch = f"{self.gitflow.prefix['hotfix']}{version}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        if not self.gitflow.branch_exists(f"{self.gitflow.origin}/{branch}"):
            raise ValueError(f"Remote branch {branch} does not exist")
            
        self.gitflow._git_command(['checkout', '-b', branch, f"{self.gitflow.origin}/{branch}"])
