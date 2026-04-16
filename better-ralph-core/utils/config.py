"""Config utility for Better Ralph Core tests"""
from pathlib import Path
from typing import Dict, Any


class Config:
    """Simple configuration class"""

    def __init__(self, config_dict: Dict[str, Any] = None):
        self.config = config_dict or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self.config[key] = value

    @classmethod
    def load_from_file(cls, file_path: Path) -> 'Config':
        """Load configuration from a file"""
        # Simplified implementation
        return cls()
