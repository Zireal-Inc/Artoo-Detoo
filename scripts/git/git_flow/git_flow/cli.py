"""
Git Flow CLI Module

This module provides the command-line interface for the Git Flow implementation.
It handles all command-line interactions and delegates the actual work to appropriate command classes.

The CLI is structured in modules:
1. Setup - Repository initialization and configuration
2. Branch - Branch management (feature, release, hotfix, etc.)
3. Issue - Issue tracking and management
4. Project - Project management integration
5. Tools - Utility functions

Usage:
    git flow setup init [--defaults] [--force]
    git flow feature start <name> [<base>]
    git flow release finish <version>
    etc.
"""

import typer
from typing import Optional
from . import __version__
from . import GitFlow
from .commands.branch import (
    FeatureCommand, ReleaseCommand, HotfixCommand, 
    SupportCommand, BugfixCommand, DevelopCommand, MasterCommand,
    SetupCommand, TaskCommand  
)
from .commands.setup import (
    InitCommand, ConfigCommand
)

COMMAND_HELP = {
    'setup': {
        'branch_prefix': {'args': ['branch_type', '[prefix]'], 'help': 'Configure branch prefix settings'},
        'config': {'args': ['action', '[section]', '[key]', '[value]'], 'help': 'Manage git-flow configuration'},
        'init': {'args': ['--defaults', '--force'], 'help': 'Initialize git-flow repository'},
        'remote': {'args': ['name', '[url]'], 'help': 'Configure remote repositories'}
    },
    'branch': {
        'bugfix': {'args': ['start/finish/publish/track/list', 'name', '[base]'], 'help': 'Manage bugfix branches'},
        'develop': {'args': ['checkout/pull/push/sync', '--rebase'], 'help': 'Manage develop branch'},
        'feature': {'args': ['start/finish/publish/track/list', 'name', '[base]'], 'help': 'Manage feature branches'},
        'hotfix': {'args': ['start/finish/publish/track/list', 'name', '[base]'], 'help': 'Manage hotfix branches'},
        'master': {'args': ['checkout/pull/push', '--rebase'], 'help': 'Manage master branch'},
        'release': {'args': ['start/finish/publish/track/list', 'name', '[base]'], 'help': 'Manage release branches'},
        'setup': {'args': ['start/finish/list', 'name', '[base]'], 'help': 'Manage setup branches'},
        'support': {'args': ['start/finish/list', 'name', '[base]'], 'help': 'Manage support branches'},
        'task': {'args': ['start/finish', 'feature', 'name', '[base]'], 'help': 'Manage task branches'}
    }
}

class SetupCommands:
    """
    Setup Command Handler
    
    Manages all setup-related commands including:
    - Repository initialization
    - Configuration management
    - Branch prefix configuration
    - Remote repository setup
    
    Attributes:
        gitflow (GitFlow): Instance of GitFlow for git operations
        app (typer.Typer): Typer instance for CLI commands
    """

    def __init__(self, gitflow: GitFlow):
        self.gitflow = gitflow
        self.app = typer.Typer()
        self._register_commands()

    def _register_commands(self):
        """Register all setup-related commands with the CLI in alphabetical order"""

        @self.app.command()
        def branch_prefix(
            branch_type: str = typer.Argument(..., help="Branch type (feature/release/hotfix/etc)"),
            prefix: Optional[str] = typer.Argument(None, help="Prefix to set")
        ):
            """
            Manage branch prefixes for different branch types
            
            Args:
                branch_type: Type of branch (feature/release/hotfix/etc)
                prefix: New prefix to set for the branch type
            """
            cmd = ConfigCommand(self.gitflow)
            if prefix:
                cmd.set("branch", branch_type, {"prefix": prefix})
            else:
                typer.echo(cmd.get("branch", branch_type))

        @self.app.command()
        def config(
            action: str = typer.Argument(..., help="Action: init, set, get, list, delete"),
            section: Optional[str] = typer.Argument(None, help="Config section"),
            key: Optional[str] = typer.Argument(None, help="Config key"),
            value: Optional[str] = typer.Argument(None, help="Config value")
        ):
            """Manage git-flow configuration"""
            cmd = ConfigCommand(self.gitflow)
            
            if action == "init":
                cmd.init()
            elif action == "set" and section and key and value:
                cmd.set(section, key, value)
            elif action == "get" and section and key:
                typer.echo(cmd.get(section, key))
            elif action == "list":
                typer.echo(cmd.list())
            elif action == "delete":
                cmd.delete()
            else:
                typer.echo(f"Invalid command or missing arguments")
                raise typer.Exit(code=1)

        @self.app.command()
        def init(
            defaults: bool = typer.Option(False, help="Use default branch names"),
            force: bool = typer.Option(False, help="Force reinitialization")
        ):
            """
            Initialize git-flow in repository
            
            Args:
                defaults: Use default settings without prompting
                force: Force reinitialization even if already initialized
            """
            cmd = InitCommand(self.gitflow)
            cmd.init(defaults=defaults, force=force)

        @self.app.command()
        def remote(
            name: str = typer.Argument(..., help="Remote name"),
            url: Optional[str] = typer.Argument(None, help="Remote URL")
        ):
            """Configure remote repositories"""
            cmd = ConfigCommand(self.gitflow)
            if url:
                cmd.set("remote", name, {"url": url})
            else:
                typer.echo(cmd.get("remote", name))

class BranchCommands:
    """
    Branch Command Handler
    
    Manages all branch-related commands including:
    - Bugfix branches
    - Develop branches
    - Feature branches
    - Release branches
    - Hotfix branches
    - Setup branches
    - Support branches
    - Task branches
    - Develop/Master management
    
    Each branch type supports standard operations:
    - start: Create new branch
    - finish: Complete and merge branch
    - publish: Push to remote
    - track: Track remote branch
    """

    def __init__(self, gitflow: GitFlow):
        self.gitflow = gitflow
        self.app = typer.Typer()
        self._register_commands()

    def _register_commands(self):
        """Register all branch-related commands with the CLI in alphabetical order"""

        @self.app.command()
        def bugfix(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish/publish/track/list"),
            name: str = typer.Argument(..., help="Bugfix name"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """Manage bugfix branches"""
            cmd = BugfixCommand(self.gitflow)
            self._handle_branch_command(cmd, subcommand, name, base)

        @self.app.command()
        def develop(
            subcommand: str = typer.Argument(..., help="Subcommand: checkout/pull/push/sync"),
            rebase: bool = typer.Option(False, help="Use rebase when pulling")
        ):
            """Manage develop branch"""
            cmd = DevelopCommand(self.gitflow)
            self._handle_develop_command(cmd, subcommand, rebase)

        @self.app.command()
        def feature(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish/publish/track/list"),
            name: str = typer.Argument(..., help="Feature name"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """Manage feature branches"""
            cmd = FeatureCommand(self.gitflow)
            self._handle_branch_command(cmd, subcommand, name, base)

        @self.app.command()
        def hotfix(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish/publish/track/list"),
            name: str = typer.Argument(..., help="Hotfix version"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """Manage hotfix branches"""
            cmd = HotfixCommand(self.gitflow)
            self._handle_branch_command(cmd, subcommand, name, base)

        @self.app.command()
        def master(
            subcommand: str = typer.Argument(..., help="Subcommand: checkout/pull/push"),
            rebase: bool = typer.Option(False, help="Use rebase when pulling")
        ):
            """Manage master branch"""
            cmd = MasterCommand(self.gitflow)
            self._handle_master_command(cmd, subcommand, rebase)

        @self.app.command()
        def release(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish/publish/track/list"),
            name: str = typer.Argument(..., help="Release version"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """Manage release branches"""
            cmd = ReleaseCommand(self.gitflow)
            self._handle_branch_command(cmd, subcommand, name, base)

        @self.app.command()
        def setup(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish/list"),
            name: str = typer.Argument(..., help="Setup branch name"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """
            Manage setup branches
            
            Used for repository setup and configuration changes
            """
            cmd = SetupCommand(self.gitflow)
            self._handle_branch_command(cmd, subcommand, name, base)

        @self.app.command()
        def support(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish/list"),
            name: str = typer.Argument(..., help="Support branch name"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """Manage long-term support branches"""
            cmd = SupportCommand(self.gitflow)
            self._handle_branch_command(cmd, subcommand, name, base)

        @self.app.command()
        def task(
            subcommand: str = typer.Argument(..., help="Subcommand: start/finish"),
            feature: str = typer.Argument(..., help="Parent feature name"),
            name: str = typer.Argument(..., help="Task name"),
            base: Optional[str] = typer.Argument(None, help="Base branch")
        ):
            """
            Manage task branches
            
            Tasks are sub-branches of features for smaller work items
            """
            cmd = TaskCommand(self.gitflow)
            try:
                if subcommand == "start":
                    cmd.start(feature, name, base)
                elif subcommand == "finish":
                    cmd.finish(feature, name)
                else:
                    typer.echo(f"Unknown subcommand: {subcommand}")
                    raise typer.Exit(code=1)
            except Exception as e:
                typer.echo(f"Error: {str(e)}")
                raise typer.Exit(code=1)

    def _handle_branch_command(self, cmd, subcommand: str, name: str, base: Optional[str] = None):
        """Handle common branch commands"""
        try:
            if subcommand == "start":
                cmd.start(name, base)
            elif subcommand == "finish":
                cmd.finish(name)
            elif subcommand == "publish":
                cmd.publish(name)
            elif subcommand == "track":
                cmd.track(name)
            elif subcommand == "list":
                branches = cmd.list(verbose=True)
                for branch, name, status, is_current in branches:
                    prefix = "* " if is_current else "  "
                    typer.echo(f"{prefix}{branch} {status}")
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(f"Error: {str(e)}")
            raise typer.Exit(code=1)

    def _handle_develop_command(self, cmd, subcommand: str, rebase: bool):
        """Handle develop branch specific commands"""
        try:
            if subcommand == "checkout":
                cmd.checkout()
            elif subcommand == "pull":
                cmd.pull(rebase=rebase)
            elif subcommand == "push":
                cmd.push()
            elif subcommand == "sync":
                cmd.sync()
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(f"Error: {str(e)}")
            raise typer.Exit(code=1)

    def _handle_master_command(self, cmd, subcommand: str, rebase: bool):
        """Handle master branch specific commands"""
        try:
            if subcommand == "checkout":
                cmd.checkout()
            elif subcommand == "pull":
                cmd.pull(rebase=rebase)
            elif subcommand == "push":
                cmd.push()
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(f"Error: {str(e)}")
            raise typer.Exit(code=1)

class CLI:
    """
    Main CLI Handler
    
    Manages the complete CLI interface including:
    - Command registration
    - Subcommand organization
    - Version information
    - Error handling
    
    The CLI follows the git-flow command pattern:
    git flow <command> <subcommand> [options]
    
    Attributes:
        app (typer.Typer): Main Typer application instance
        gitflow (GitFlow): GitFlow instance for git operations
        setup (SetupCommands): Setup command handler
    """

    def __init__(self):
        """Initialize CLI with necessary components"""
        self.app = typer.Typer(help=self._generate_help_text())
        self.gitflow = GitFlow()
        self.setup = SetupCommands(self.gitflow)
        self.branch = BranchCommands(self.gitflow)
        self._register_commands()

    def _generate_help_text(self) -> str:
        """Generate comprehensive help text including command listing"""
        help_text = [
            "Git Flow - A collection of Git extensions to provide high-level repository operations\n",
            "Provides structured branching model operations through command-line interface. \n",
            "Use --help with any command for detailed usage information. \n\n",
            "Available Commands:\n"
        ]
        
        # Add setup commands
        # help_text.append("Setup Commands:")
        # for cmd, details in COMMAND_HELP['setup'].items():
        #     args = ' '.join(details['args'])
        #     help_text.append(f"  git flow setup {cmd} {args}")
        #     help_text.append(f"    {details['help']}\n")
        
        # Add branch commands
        # help_text.append("Branch Commands:")
        # for cmd, details in COMMAND_HELP['branch'].items():
        #     args = ' '.join(details['args'])
        #     help_text.append(f"  git flow branch {cmd} {args}")
        #     help_text.append(f"    {details['help']}\n")
        
        return "\n".join(help_text)

    def _register_commands(self):
        """
        Register all available commands with the CLI
        
        Organizes commands into logical groups:
        - Setup commands (init, config)
        - Branch commands (feature, release, hotfix, etc.)
        - Project commands
        - Tool commands
        """
        
        # Add setup and branch commands as sub-applications
        self.app.add_typer(self.setup.app, name="setup", help="Setup commands")
        self.app.add_typer(self.branch.app, name="branch", help="Branch management commands")

        # @self.app.command(name="commands")
        # def list_commands():
        #     """List all available commands and their usage"""
        #     typer.echo(self._generate_help_text())

        @self.app.callback()
        def main(
            version: bool = typer.Option(
                None, "--version",
                callback=lambda value: typer.echo(f"git-flow {__version__}") if value else None,
                is_eager=True
            )
        ):
            """
            Git Flow - A collection of Git extensions to provide high-level repository operations
            
            Provides structured branching model operations through command-line interface.
            Use --help with any command for detailed usage information.
            """
            pass

    def run(self):
        """Execute the CLI application"""
        self.app()

if __name__ == "__main__":
    cli = CLI()
    cli.run()
