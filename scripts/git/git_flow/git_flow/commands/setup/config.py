from typing import Dict, Any, Optional
from ...settings import Settings
from .base import BaseCommand
import re

class ConfigCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Settings(self.gitflow.config_path)

    def validate_section_key(self, section: str, key: str) -> bool:
        """Validate section and key names"""
        return bool(re.match(r'^[a-zA-Z0-9_.]+$', section) and 
                   re.match(r'^[a-zA-Z0-9_]+$', key))

    def init(self, initial_values: Optional[Dict[str, Any]] = None) -> None:
        """Initialize config file"""
        self.settings.create_config(initial_values)

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
