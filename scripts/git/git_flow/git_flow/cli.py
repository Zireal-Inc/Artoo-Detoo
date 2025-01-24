import typer
from typing import Optional
from . import __version__
from . import GitFlow
from .commands.branch import (
    FeatureCommand, ReleaseCommand, HotfixCommand, 
    SupportCommand, BugfixCommand
)

from .commands.setup import (
    InitCommand, ConfigCommand
)

class SetupCommands:
    def __init__(self, gitflow: GitFlow):
        self.gitflow = gitflow
        self.app = typer.Typer()
        self._register_commands()

    def _register_commands(self):
        @self.app.command()
        def init(
            defaults: bool = typer.Option(False, help="Use default branch names"),
            force: bool = typer.Option(False, help="Force reinitialization")
        ):
            """Initialize git-flow in repository"""
            cmd = InitCommand(self.gitflow)
            cmd.init(defaults=defaults, force=force)

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
        def branch_prefix(
            branch_type: str = typer.Argument(..., help="Branch type (feature/release/hotfix/etc)"),
            prefix: Optional[str] = typer.Argument(None, help="Prefix to set")
        ):
            """Manage branch prefixes"""
            cmd = ConfigCommand(self.gitflow)
            if prefix:
                cmd.set("branch", branch_type, {"prefix": prefix})
            else:
                typer.echo(cmd.get("branch", branch_type))

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

class CLI:
    def __init__(self):
        self.app = typer.Typer()
        self.gitflow = GitFlow()
        self.setup = SetupCommands(self.gitflow)
        self._register_commands()

    def _register_commands(self):
        # Add setup commands as a sub-application
        self.app.add_typer(self.setup.app, name="setup", help="Setup commands")

        @self.app.command()
        def feature(
            subcommand: str = typer.Argument(..., help="Subcommand: start or finish"),
            name: str = typer.Argument(..., help="Feature name"),
            base: str = typer.Argument(None, help="Base branch")
        ):
            cmd = FeatureCommand(self.gitflow)
            if subcommand == "start":
                cmd.start(name, base)
            elif subcommand == "finish":
                cmd.finish(name)
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)

        @self.app.command()
        def release(
            subcommand: str = typer.Argument(..., help="Subcommand: start or finish"),
            name: str = typer.Argument(..., help="Release name"),
            base: str = typer.Argument(None, help="Base branch")
        ):
            cmd = ReleaseCommand(self.gitflow)
            if subcommand == "start":
                cmd.start(name, base)
            elif subcommand == "finish":
                cmd.finish(name)
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)

        @self.app.command()
        def hotfix(
            subcommand: str = typer.Argument(..., help="Subcommand: start or finish"),
            version: str = typer.Argument(..., help="Hotfix version"),
            base: str = typer.Argument(None, help="Base branch")
        ):
            cmd = HotfixCommand(self.gitflow)
            if subcommand == "start":
                cmd.start(version, base)
            elif subcommand == "finish":
                cmd.finish(version)
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)

        @self.app.command()
        def support(
            subcommand: str = typer.Argument(..., help="Subcommand: start or finish"),
            name: str = typer.Argument(..., help="Support name"),
            base: str = typer.Argument(None, help="Base branch")
        ):
            cmd = SupportCommand(self.gitflow)
            if subcommand == "start":
                cmd.start(name, base)
            elif subcommand == "finish":
                cmd.finish(name)
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)

        @self.app.command()
        def bugfix(
            subcommand: str = typer.Argument(..., help="Subcommand: start or finish"),
            name: str = typer.Argument(..., help="Bugfix name"),
            base: str = typer.Argument(None, help="Base branch")
        ):
            cmd = BugfixCommand(self.gitflow)
            if subcommand == "start":
                cmd.start(name, base)
            elif subcommand == "finish":
                cmd.finish(name)
            else:
                typer.echo(f"Unknown subcommand: {subcommand}")
                raise typer.Exit(code=1)

        @self.app.callback()
        def main(
            version: bool = typer.Option(
                None, "--version",
                callback=lambda value: typer.echo(f"git-flow {__version__}") if value else None,
                is_eager=True
            )
        ):
            """Git Flow command line interface"""
            pass

    def run(self):
        self.app()

if __name__ == "__main__":
    cli = CLI()
    cli.run()
