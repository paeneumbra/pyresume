from pathlib import Path
from typing import List

from pyresume.settings import ASSETS_DIR


class CssStyles:
    """Manages CSS style files"""

    styles_dir = ASSETS_DIR / "styles"
    DEFAULT_STYLE_NAME = "simple-style"

    @classmethod
    def get_style_path(cls, style_name: str) -> Path:
        """Get the full path to a style file by name"""
        return cls.styles_dir / f"{style_name}.css"

    @classmethod
    def get_styles(cls) -> List[str]:
        """Get all available style names without extension"""
        if not cls.styles_dir.exists():
            return []

        style_files = cls.styles_dir.glob("*.css")
        style_names = [style_file.stem for style_file in style_files]
        return sorted(style_names)

    @classmethod
    def print_styles(cls) -> None:
        """Print all available styles"""
        style_names = cls.get_styles()
        print("\033[1;32mAvailable styles\033[0m:")
        print(" >", "\n > ".join(style_names))

    @property
    def bar_style(self) -> str:
        return str(self.get_style_path("bar-style"))

    @property
    def divider_style(self) -> str:
        return str(self.get_style_path("divider-style"))

    @property
    def simple_style(self) -> str:
        return str(self.get_style_path("simple-style"))

    @property
    def default_style(self) -> str:
        return str(self.get_style_path(self.DEFAULT_STYLE_NAME))
