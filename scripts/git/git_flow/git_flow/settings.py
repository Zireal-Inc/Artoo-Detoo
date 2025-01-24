import os
import toml
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    'user': {
        'name': '',
        'email': ''
    },
    'branch': {
        'main': {'prefix': '', 'url': '', 'default': 'main'},
        'develop': {'prefix': '', 'url': '', 'default': 'develop'},
        'feature': {'prefix': 'feature/', 'url': '', 'default': ''},
        'bugfix': {'prefix': 'bugfix/', 'url': '', 'default': ''},
        'hotfix': {'prefix': 'hotfix/', 'url': '', 'default': ''},
        'release': {'prefix': 'release/', 'url': '', 'default': ''},
        'support': {'prefix': 'support/', 'url': '', 'default': ''},
        'version': {'prefix': 'v', 'url': '', 'default': ''},
        'task': {'prefix': 'task/', 'url': '', 'default': ''},
        'default': {'prefix': '', 'url': '', 'default': ''}
    },
    'remote': {
        'origin': {
            'main': '',
            'develop': '',
            'feature': '',
            'hotfix': '',
            'release': '',
            'support': ''
        },
        'upstream': '',
        'prefix': {'origin': '', 'upstream': ''},
        'url': {'origin': '', 'upstream': ''},
        'default': 'origin'
    },
    'config': {}
}

class Settings:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.read_config()

    def create_config(self, initial_values: Optional[Dict[str, Any]] = None) -> None:
        """Create a new config file with default or initial values"""
        if os.path.exists(self.config_path):
            raise FileExistsError("Config file already exists")
        
        config = DEFAULT_CONFIG.copy()
        if initial_values:
            self._deep_update(config, initial_values)
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        self.write_config(config)

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate config structure"""
        try:
            required_sections = ['user', 'branch', 'remote', 'config']
            return all(section in config for section in required_sections)
        except Exception:
            return False

    def read_config(self) -> Dict[str, Any]:
        """Read the config file"""
        try:
            if not os.path.exists(self.config_path):
                return {}
            with open(self.config_path, 'r') as f:
                config = toml.load(f)
                if not self.validate_config(config):
                    raise ValueError("Invalid config structure")
                return config
        except Exception as e:
            raise IOError(f"Error reading config: {str(e)}")

    def write_config(self, config: Dict[str, Any]) -> None:
        """Write the config file"""
        try:
            if not self.validate_config(config):
                raise ValueError("Invalid config structure")
            with open(self.config_path, 'w') as f:
                toml.dump(config, f)
        except Exception as e:
            raise IOError(f"Error writing config: {str(e)}")

    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update config with new values"""
        self._deep_update(self.config, updates)
        self.write_config(self.config)

    def delete_config(self) -> None:
        """Delete the config file"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def _deep_update(self, base: Dict, updates: Dict) -> None:
        """Recursively update nested dictionaries"""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base:
                self._deep_update(base[key], value)
            else:
                base[key] = value
