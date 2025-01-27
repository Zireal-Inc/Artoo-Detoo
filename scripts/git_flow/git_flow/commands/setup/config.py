from typing import Dict, Any, Optional
import re
import typer
from rich.prompt import Prompt, Confirm
from ...settings import Settings
from ..base import BaseCommand

class GitFlowError(Exception):
    pass

# Move ConfigCommand to a separate file to avoid circular imports

class ConfigCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Settings(self.gitflow.config_path)

    def validate_section_key(self, section: str, key: str) -> bool:
        """Validate section and key names"""
        return bool(re.match(r'^[a-zA-Z0-9_.]+$', section) and 
                   re.match(r'^[a-zA-Z0-9_]+$', key))

    def init(self, initial_values: Optional[Dict[str, Any]] = None, interactive: bool = True) -> None:
        """Initialize config file interactively"""
        config = {}
        
        if interactive:
            typer.echo(f"\nChecking configuration at: {self.gitflow.config_path}")
            if self.settings.config_exists():
                typer.echo(f"Configuration already exists at: {self.gitflow.config_path}")
                if not Confirm.ask("Do you want to reconfigure?", default=False):
                    return

            # User configuration
            typer.echo("\nConfiguring user settings...")
            config['user'] = {
                'name': Prompt.ask("Enter your Git username", default=""),
                'email': Prompt.ask("Enter your Git email", default="")
            }

            # Remote configuration
            typer.echo("\nConfiguring remote settings...")
            use_remote = Confirm.ask("Do you want to configure remote repositories?", default=True)
            if use_remote:
                config['remote'] = {
                    'default': Prompt.ask("Default remote name", default="origin"),
                    'prefix': {
                        'origin': Prompt.ask("Origin prefix", default=""),
                        'upstream': Prompt.ask("Upstream prefix", default="")
                    },
                    'url': {
                        'origin': Prompt.ask("Origin URL", default=""),
                        'upstream': Prompt.ask("Upstream URL", default="")
                    }
                }

            # Branch configuration
            typer.echo("\nConfiguring branch settings...")
            branch_types = ['main', 'develop', 'feature', 'bugfix', 'hotfix', 
                          'release', 'support', 'version', 'task']
            
            config['branch'] = {}
            for branch_type in branch_types:
                typer.echo(f"\nConfiguring {branch_type} branch settings...")
                config['branch'][branch_type] = {
                    'prefix': Prompt.ask(
                        f"{branch_type} branch prefix",
                        default=self.settings.DEFAULT_CONFIG['branch'][branch_type]['prefix']
                    ),
                    'url': Prompt.ask(
                        f"{branch_type} URL",
                        default=""
                    ),
                    'default': Prompt.ask(
                        f"Default {branch_type} branch name",
                        default=self.settings.DEFAULT_CONFIG['branch'][branch_type]['default']
                    ),
                    'remote': {
                        'enabled': Confirm.ask(
                            f"Enable remote tracking for {branch_type} branches?",
                            default=self.settings.DEFAULT_CONFIG['branch'][branch_type]['remote']['enabled']
                        ),
                        'upstream': Prompt.ask(
                            f"Upstream remote for {branch_type}",
                            default=""
                        ),
                        'origin': Prompt.ask(
                            f"Origin remote for {branch_type}",
                            default=""
                        ),
                        'push_on_finish': Confirm.ask(
                            f"Push {branch_type} branches on finish?",
                            default=self.settings.DEFAULT_CONFIG['branch'][branch_type]['remote']['push_on_finish']
                        ),
                        'track': Confirm.ask(
                            f"Track remote {branch_type} branches?",
                            default=self.settings.DEFAULT_CONFIG['branch'][branch_type]['remote']['track']
                        )
                    }
                }

            # Default branch configuration
            config['branch']['default'] = self.settings.DEFAULT_CONFIG['branch']['default']

        # Merge with initial values if provided
        if initial_values:
            self._deep_update(config, initial_values)

        # Create config with collected values
        self.settings.create_config(config)
        typer.echo(f"\nConfiguration completed successfully!")
        typer.echo(f"Configuration file created at: {self.gitflow.config_path}")

    def set(self, section: str, key: str, value: str) -> None:
        """Set a config value"""
        if not self.validate_section_key(section, key):
            raise ValueError("Invalid section or key name")
        try:
            updates = {}
            parts = section.split('.')
            current = updates
            for part in parts[:-1]:
                current[part] = {}
                current = current[part]
            current[parts[-1]] = {key: value}
            self.settings.update_config(updates)
        except Exception as e:
            raise GitFlowError(f"Failed to set config: {str(e)}")

    def get(self, section: str, key: str) -> Any:
        """Get a config value"""
        config = self.settings.read_config()
        current = config
        for part in section.split('.'):
            current = current.get(part, {})
        return current.get(key)

    def list(self) -> Dict[str, Any]:
        """List all config values"""
        return self.settings.read_config()

    def delete(self) -> None:
        """Delete config file"""
        self.settings.delete_config()

