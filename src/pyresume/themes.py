"""Theme discovery and CSS path resolution."""

from pathlib import Path


RESOURCES_DIR = Path(__file__).parent / "resources"
THEMES_DIR = RESOURCES_DIR / "themes"

BUILT_IN_THEMES = {
    "minimal": "minimal.css",
    "clean": "clean.css",
    "slate": "slate.css",
}


def get_theme_path(theme_name: str) -> Path:
    """Get path to built-in theme CSS file.

    Args:
        theme_name: Name of built-in theme (minimal, clean, slate)

    Returns:
        Path to CSS file

    Raises:
        ValueError: If theme not found
    """
    if theme_name not in BUILT_IN_THEMES:
        raise ValueError(
            f"Unknown theme: {theme_name}. Available: {', '.join(BUILT_IN_THEMES.keys())}"
        )

    css_file = THEMES_DIR / BUILT_IN_THEMES[theme_name]
    if not css_file.exists():
        raise FileNotFoundError(f"Theme CSS file not found: {css_file}")

    return css_file


def list_themes() -> list[str]:
    """Return list of available built-in theme names."""
    return sorted(BUILT_IN_THEMES.keys())


def resolve_css(
    theme: str | None = None,
    css_path: str | None = None,
) -> Path | None:
    """Resolve CSS path from theme name or custom path.

    Args:
        theme: Built-in theme name
        css_path: Custom CSS file path

    Returns:
        Path to CSS file, or None if neither provided

    Raises:
        ValueError: If theme is invalid
        FileNotFoundError: If CSS path doesn't exist
    """
    if css_path:
        css_file = Path(css_path)
        if not css_file.exists():
            raise FileNotFoundError(f"CSS file not found: {css_path}")
        return css_file

    if theme:
        return get_theme_path(theme)

    return None
