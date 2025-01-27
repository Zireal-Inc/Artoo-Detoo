import os
import yaml
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    'user': {
        'name': '',
        'email': ''
    },
    'remote': {
        'default': 'origin',
        'prefix': {
            'origin': '',
            'upstream': ''
        },
        'url': {
            'origin': '',
            'upstream': ''
        }
    },
    'config': {},
    'branch': {
        'main': {
            'prefix': '',
            'url': '',
            'default': 'main',
            'remote': {
                'enabled': False,
                'upstream': '',
                'origin': '',
                'push_on_finish': False,
                'track': True
            }
        },
        'develop': {
            'prefix': '',
            'url': '',
            'default': 'develop',
            'remote': {
                'enabled': False,
                'upstream': '',
                'origin': '',
                'push_on_finish': False,
                'track': True
            }
        },
        'feature': {
            'prefix': 'feature-',
            'url': '',
            'default': '',
            'remote': {
                'enabled': True,
                'upstream': '',
                'origin': '',
                'push_on_finish': True,
                'track': True
            }
        },
        'bugfix': {
            'prefix': 'bugfix-',
            'url': '',
            'default': '',
            'remote': {
                'enabled': True,
                'upstream': '',
                'origin': '',
                'push_on_finish': True,
                'track': True
            }
        },
        'hotfix': {
            'prefix': 'hotfix-',
            'url': '',
            'default': '',
            'remote': {
                'enabled': True,
                'upstream': '',
                'origin': '',
                'push_on_finish': True,
                'track': True
            }
        },
        'release': {
            'prefix': 'release-',
            'url': '',
            'default': '',
            'remote': {
                'enabled': True,
                'upstream': '',
                'origin': '',
                'push_on_finish': True,
                'track': True
            }
        },
        'support': {
            'prefix': 'support-',
            'url': '',
            'default': '',
            'remote': {
                'enabled': True,
                'upstream': '',
                'origin': '',
                'push_on_finish': True,
                'track': True
            }
        },
        'version': {
            'prefix': 'v',
            'url': '',
            'default': '',
            'remote': {
                'enabled': False,
                'upstream': '',
                'origin': '',
                'push_on_finish': False,
                'track': False
            }
        },
        'task': {
            'prefix': 'task-',
            'url': '',
            'default': '',
            'remote': {
                'enabled': True,
                'upstream': '',
                'origin': '',
                'push_on_finish': True,
                'track': True
            }
        },
        'default': {
            'prefix': '',
            'url': '',
            'default': '',
            'remote': {
                'enabled': False,
                'upstream': '',
                'origin': '',
                'push_on_finish': False,
                'track': False
            }
        }
    }
}

class Settings:
    # Make DEFAULT_CONFIG accessible as a class attribute
    DEFAULT_CONFIG = DEFAULT_CONFIG

    def __init__(self, config_path: str):
        """Initialize Settings with config path"""
        self.config_path = config_path #self._update_config_extension(config_path)
        self.config = self.read_config()

    def config_exists(self) -> bool:
        """Check if config file exists"""
        return os.path.exists(self.config_path)

    def _update_config_extension(self, path: str) -> str:
        """Update config file extension from .toml to .yaml"""
        return path.replace('.toml', '.yaml')

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
        """Read the YAML config file"""
        try:
            if not os.path.exists(self.config_path):
                return {}
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                if not self.validate_config(config):
                    raise ValueError("Invalid config structure")
                return config
        except Exception as e:
            raise IOError(f"Error reading config: {str(e)}")

    def write_config(self, config: Dict[str, Any]) -> None:
        """Write the YAML config file"""
        try:
            if not self.validate_config(config):
                raise ValueError("Invalid config structure")
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
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
