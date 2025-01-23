from typing import Optional, List, Tuple
from .base import BaseCommand

class ReleaseCommand(BaseCommand):
    def start(self, version: str, base: Optional[str] = None):
        """Start a new release branch"""
        if base is None:
            base = self.gitflow.develop_branch
            
        branch = f"{self.gitflow.prefix['release']}{version}"
        version_tag = f"{self.gitflow.prefix['version']}{version}"
        
        # Sanity checks
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        # Check for existing release branches
        for existing in self.gitflow.get_branches():
            if existing.startswith(self.gitflow.prefix['release']):
                raise ValueError(f"There is an existing release branch ({existing}). Finish that one first.")
                
        # Check if version tag exists
        if version_tag in self.gitflow.get_all_tags():
            raise ValueError(f"Tag {version_tag} already exists")
            
        self.gitflow.create_branch(branch, base)

    def finish(self, version: str, tag_message: Optional[str] = None, sign: bool = False, 
              push: bool = False, keep: bool = False, squash: bool = False, 
              signing_key: Optional[str] = None, no_tag: bool = False):
        """Finish a release branch"""
        branch = f"{self.gitflow.prefix['release']}{version}"
        version_tag = f"{self.gitflow.prefix['version']}{version}"
        
        if not self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} does not exist")
            
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        # Merge into master
        if not self.gitflow.is_branch_merged_into(branch, self.gitflow.master_branch):
            self.gitflow._git_command(['checkout', self.gitflow.master_branch])
            if squash:
                self.gitflow._git_command(['merge', '--squash', branch])
                self.gitflow._git_command(['commit'])
            else:
                self.gitflow.merge_branch(branch)
                
        # Create tag
        if not no_tag and not version_tag in self.gitflow.get_all_tags():
            tag_args = ['tag', '-a']
            if sign:
                tag_args.append('-s')
            if signing_key:
                tag_args.extend(['-u', signing_key])
            if tag_message:
                tag_args.extend(['-m', tag_message])
            tag_args.extend([version_tag, branch])
            self.gitflow._git_command(tag_args)
            
        # Merge into develop
        if not self.gitflow.is_branch_merged_into(branch, self.gitflow.develop_branch):
            self.gitflow._git_command(['checkout', self.gitflow.develop_branch])
            if squash:
                self.gitflow._git_command(['merge', '--squash', branch])
                self.gitflow._git_command(['commit'])
            else:
                self.gitflow.merge_branch(branch)
                
        # Delete branch
        if not keep:
            if self.gitflow.get_current_branch() == branch:
                self.gitflow._git_command(['checkout', self.gitflow.master_branch])
            self.gitflow.delete_branch(branch)
            
        # Push changes
        if push:
            self.gitflow._git_command(['push', self.gitflow.origin, self.gitflow.develop_branch])
            self.gitflow._git_command(['push', self.gitflow.origin, self.gitflow.master_branch])
            if not no_tag:
                self.gitflow._git_command(['push', '--tags', self.gitflow.origin])
            self.gitflow._git_command(['push', self.gitflow.origin, f":{branch}"])

    def list(self, verbose: bool = False) -> List[Tuple[str, str, str, bool]]:
        """List all release branches"""
        release_branches = []
        current = self.gitflow.get_current_branch()
        
        for branch in self.gitflow.get_branches():
            if not branch.startswith(self.gitflow.prefix['release']):
                continue
                
            name = branch[len(self.gitflow.prefix['release']):]
            if verbose:
                base = self.gitflow._git_command(['merge-base', branch, self.gitflow.develop_branch]).strip()
                develop_sha = self.gitflow._git_command(['rev-parse', self.gitflow.develop_branch]).strip()
                branch_sha = self.gitflow._git_command(['rev-parse', branch]).strip()
                
                status = ""
                if branch_sha == develop_sha:
                    status = "(no commits yet)"
                else:
                    base_sha = self.gitflow._git_command(['rev-parse', '--short', base]).strip()
                    status = f"(based on {base_sha})"
                    
                release_branches.append((branch, name, status, branch == current))
            else:
                release_branches.append((branch, name, "", branch == current))
                
        return release_branches

    def publish(self, version: str):
        """Publish release branch to remote"""
        branch = f"{self.gitflow.prefix['release']}{version}"
        
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
        """Track remote release branch"""
        branch = f"{self.gitflow.prefix['release']}{version}"
        
        if not self.gitflow.is_clean_working_tree():
            raise ValueError("Working tree is not clean")
            
        if self.gitflow.branch_exists(branch):
            raise ValueError(f"Branch {branch} already exists")
            
        if not self.gitflow.branch_exists(f"{self.gitflow.origin}/{branch}"):
            raise ValueError(f"Remote branch {branch} does not exist")
            
        self.gitflow._git_command(['checkout', '-b', branch, f"{self.gitflow.origin}/{branch}"])
