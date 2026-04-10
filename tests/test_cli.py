"""Tests for CLI module."""

import pytest
from typer.testing import CliRunner

from pyresume.cli import app

runner = CliRunner()


@pytest.fixture
def markdown_file(tmp_path):
    """Create a temporary markdown file."""
    md = tmp_path / "resume.md"
    md.write_text("# Test Resume\n\nContent here.")
    return md


@pytest.fixture
def css_file(tmp_path):
    """Create a temporary CSS file."""
    css = tmp_path / "style.css"
    css.write_text("body { font-size: 10pt; }")
    return css


def test_cli_list_themes():
    """Test --list flag."""
    result = runner.invoke(app, ["--list"])
    assert result.exit_code == 0
    assert "minimal" in result.stdout
    assert "clean" in result.stdout
    assert "slate" in result.stdout


def test_cli_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "markdown" in result.stdout.lower()


def test_cli_with_markdown_default_theme(markdown_file, tmp_path):
    """Test CLI with markdown file and default theme."""
    result = runner.invoke(app, [str(markdown_file)])
    assert result.exit_code == 0
    assert "PDF generated" in result.stdout


def test_cli_with_minimal_theme(markdown_file):
    """Test CLI with --minimal theme."""
    result = runner.invoke(app, [str(markdown_file), "--minimal"])
    assert result.exit_code == 0
    assert "PDF generated" in result.stdout


def test_cli_with_clean_theme(markdown_file):
    """Test CLI with --clean theme."""
    result = runner.invoke(app, [str(markdown_file), "--clean"])
    assert result.exit_code == 0
    assert "PDF generated" in result.stdout


def test_cli_with_custom_css(markdown_file, css_file):
    """Test CLI with custom CSS file."""
    result = runner.invoke(app, [str(markdown_file), "--css", str(css_file)])
    assert result.exit_code == 0
    assert "PDF generated" in result.stdout


def test_cli_multiple_themes_error(markdown_file):
    """Test error when multiple theme flags provided."""
    result = runner.invoke(app, [str(markdown_file), "--minimal", "--clean"])
    assert result.exit_code == 1
    assert "Only one theme" in result.stdout


def test_cli_theme_and_css_error(markdown_file, css_file):
    """Test error when both theme flag and --css provided."""
    result = runner.invoke(
        app, [str(markdown_file), "--minimal", "--css", str(css_file)]
    )
    assert result.exit_code == 1
    assert "Cannot use both" in result.stdout


def test_cli_nonexistent_markdown():
    """Test error on nonexistent markdown file."""
    result = runner.invoke(app, ["/nonexistent/resume.md"])
    assert result.exit_code != 0
