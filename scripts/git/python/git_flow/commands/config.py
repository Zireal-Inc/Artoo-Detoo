from typing import Dict, Any, Optional
from ..settings import Settings
from .base import BaseCommand

class ConfigCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Settings(self.gitflow.config_path)

    def init(self, initial_values: Optional[Dict[str, Any]] = None) -> None:
        """Initialize config file"""
        self.settings.create_config(initial_values)

    def set(self, section: str, key: str, value: str) -> None:
        """Set a config value"""
        updates = {}
        parts = section.split('.')
        current = updates
        for part in parts[:-1]:
            current[part] = {}
            current = current[part]
        current[parts[-1]] = {key: value}
        self.settings.update_config(updates)

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
