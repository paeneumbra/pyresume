"""Tests for themes module."""

import pytest

from pyresume.themes import (
    BUILT_IN_THEMES,
    get_theme_path,
    list_themes,
    resolve_css,
)


def test_list_themes():
    """Test listing available themes."""
    themes = list_themes()
    assert isinstance(themes, list)
    assert len(themes) > 0
    assert "minimal" in themes
    assert "clean" in themes
    assert "slate" in themes


def test_list_themes_sorted():
    """Test that themes are sorted."""
    themes = list_themes()
    assert themes == sorted(themes)


@pytest.mark.parametrize("theme", list(BUILT_IN_THEMES.keys()))
def test_get_theme_path(theme):
    """Test getting path for each built-in theme."""
    path = get_theme_path(theme)
    assert path.exists()
    assert path.suffix == ".css"
    assert theme in path.name


def test_get_theme_path_invalid():
    """Test error on invalid theme name."""
    with pytest.raises(ValueError, match="Unknown theme"):
        get_theme_path("nonexistent")


@pytest.mark.parametrize("theme", list(BUILT_IN_THEMES.keys()))
def test_resolve_css_with_theme(theme):
    """Test resolving CSS via each built-in theme."""
    path = resolve_css(theme=theme)
    assert path is not None
    assert path.exists()


def test_resolve_css_with_custom_path(tmp_path):
    """Test resolving CSS via custom file path."""
    css_file = tmp_path / "custom.css"
    css_file.write_text("body { color: red; }")
    path = resolve_css(css_path=str(css_file))
    assert path == css_file


def test_resolve_css_nonexistent_custom():
    """Test error when custom CSS file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        resolve_css(css_path="/nonexistent/path.css")


def test_resolve_css_none():
    """Test resolving CSS with no arguments returns None."""
    path = resolve_css()
    assert path is None


def test_resolve_css_prefers_custom():
    """Test that custom CSS path takes precedence over theme."""
    # This should fail because the path doesn't exist, proving it tried custom first
    with pytest.raises(FileNotFoundError):
        resolve_css(theme="minimal", css_path="/nonexistent/path.css")
