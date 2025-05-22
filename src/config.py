"""
Configuration management for the plotting package.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class PlottingConfig:
    """
    Configuration class for plotting settings.
    
    This class holds default values for font settings, DPI, colors,
    and other plotting parameters that can be customized by users.
    """
    
    # Font settings
    default_font: str = 'Arial'
    font_sizes: Dict[str, int] = None
    
    # Figure settings
    dpi: int = 300
    default_width: float = 10.0  # cm
    default_height: float = 8.0  # cm
    default_unit: str = 'cm'
    
    # Style settings
    spine_width: float = 1.4
    grid_color: str = 'C7'
    grid_style: str = '--'
    grid_width: float = 0.8
    
    # Color schemes
    color_palette: str = 'deep'
    
    def __post_init__(self):
        """Initialize default font sizes if not provided."""
        if self.font_sizes is None:
            self.font_sizes = {
                'small': 8,
                'medium': 10,
                'big': 12
            }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'PlottingConfig':
        """
        Create a configuration from a dictionary.
        
        Args:
            config_dict: Dictionary containing configuration parameters.
            
        Returns:
            PlottingConfig instance.
        """
        return cls(**config_dict)
    
    @classmethod
    def from_json(cls, json_path: Path) -> 'PlottingConfig':
        """
        Load configuration from a JSON file.
        
        Args:
            json_path: Path to the JSON configuration file.
            
        Returns:
            PlottingConfig instance.
            
        Raises:
            FileNotFoundError: If the JSON file doesn't exist.
            json.JSONDecodeError: If the JSON file is malformed.
        """
        with open(json_path, 'r') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.
        
        Returns:
            Dictionary representation of the configuration.
        """
        return {
            'default_font': self.default_font,
            'font_sizes': self.font_sizes,
            'dpi': self.dpi,
            'default_width': self.default_width,
            'default_height': self.default_height,
            'default_unit': self.default_unit,
            'spine_width': self.spine_width,
            'grid_color': self.grid_color,
            'grid_style': self.grid_style,
            'grid_width': self.grid_width,
            'color_palette': self.color_palette,
        }
    
    def to_json(self, json_path: Path) -> None:
        """
        Save configuration to a JSON file.
        
        Args:
            json_path: Path where to save the JSON configuration file.
        """
        with open(json_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def update(self, **kwargs) -> None:
        """
        Update configuration parameters.
        
        Args:
            **kwargs: Configuration parameters to update.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration parameter: {key}")
    
    def get_journal_preset(self, journal: str) -> 'PlottingConfig':
        """
        Get configuration preset for specific journals.
        
        Args:
            journal: Journal name (e.g., 'nature', 'science', 'cell').
            
        Returns:
            PlottingConfig instance configured for the specified journal.
            
        Raises:
            ValueError: If journal preset is not available.
        """
        presets = {
            'nature': {
                'default_font': 'Arial',
                'font_sizes': {'small': 7, 'medium': 8, 'big': 9},
                'default_width': 8.3,  # Single column width
                'default_height': 6.0,
                'spine_width': 1.0,
            },
            'science': {
                'default_font': 'Arial',
                'font_sizes': {'small': 7, 'medium': 8, 'big': 9},
                'default_width': 8.5,
                'default_height': 6.5,
                'spine_width': 1.2,
            },
            'cell': {
                'default_font': 'Arial',
                'font_sizes': {'small': 8, 'medium': 9, 'big': 10},
                'default_width': 17.8,  # Full page width
                'default_height': 12.0,
                'spine_width': 1.4,
            },
            'plos_one': {
                'default_font': 'Arial',
                'font_sizes': {'small': 8, 'medium': 10, 'big': 12},
                'default_width': 17.4,
                'default_height': 12.0,
                'spine_width': 1.5,
            }
        }
        
        if journal.lower() not in presets:
            available = ', '.join(presets.keys())
            raise ValueError(f"Journal '{journal}' not available. Available presets: {available}")
        
        # Create a copy of current config and update with preset
        config_dict = self.to_dict()
        config_dict.update(presets[journal.lower()])
        
        return PlottingConfig.from_dict(config_dict)
    
    def __str__(self) -> str:
        """String representation of the configuration."""
        return f"PlottingConfig(font={self.default_font}, dpi={self.dpi}, size={self.default_width}x{self.default_height}{self.default_unit})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the configuration."""
        return f"PlottingConfig({self.to_dict()})"


# Predefined configurations for common use cases
DEFAULT_CONFIG = PlottingConfig()

MINIMAL_CONFIG = PlottingConfig(
    font_sizes={'small': 6, 'medium': 8, 'big': 10},
    default_width=6.0,
    default_height=4.5
)

HIGH_RES_CONFIG = PlottingConfig(
    dpi=600,
    font_sizes={'small': 10, 'medium': 12, 'big': 14},
    default_width=15.0,
    default_height=12.0
)