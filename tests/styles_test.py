from pathlib import Path

import pytest

from pyresume.css_styles import CssStyles
from pyresume.settings import ASSETS_DIR


@pytest.fixture(scope="module")
def css_styles():
    return CssStyles()


class TestStylePaths:
    """Test that style properties return correct file paths"""

    @pytest.mark.parametrize(
        "style_attr,filename",
        [
            ("simple_style", "simple-style.css"),
            ("bar_style", "bar-style.css"),
            ("divider_style", "divider-style.css"),
            ("default_style", "simple-style.css"),  # default points to simple
        ],
    )
    def test_style_path_and_existence(self, css_styles, style_attr, filename):
        style = getattr(css_styles, style_attr)
        expected_path = ASSETS_DIR / "styles" / filename

        assert style == str(expected_path), f"{style_attr} path mismatch"
        assert Path(style).exists(), f"{filename} file does not exist"


class TestStyleListing:
    """Test style enumeration and display"""

    def test_get_styles_returns_sorted_names(self, css_styles):
        names = css_styles.get_styles()
        expected_styles = ["bar-style", "divider-style", "simple-style"]

        assert names == expected_styles
        assert names == sorted(names), "Styles should be sorted"

    def test_print_styles_output(self, capsys, css_styles):
        css_styles.print_styles()

        captured = capsys.readouterr()
        assert "Available styles" in captured.out

        for style in ["bar-style", "divider-style", "simple-style"]:
            assert style in captured.out, f"Style '{style}' not in output"
