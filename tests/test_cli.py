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


@pytest.mark.parametrize(
    "theme_flag",
    [None, "--minimal", "--clean", "--slate"],
)
def test_cli_with_theme(markdown_file, tmp_path, monkeypatch, theme_flag):
    """Test CLI with various theme flags (or default)."""
    monkeypatch.chdir(tmp_path)
    args = [str(markdown_file)]
    if theme_flag:
        args.append(theme_flag)
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "PDF generated" in result.stdout


def test_cli_with_custom_css(markdown_file, css_file, tmp_path, monkeypatch):
    """Test CLI with custom CSS file."""
    monkeypatch.chdir(tmp_path)
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


def test_cli_with_output_dir(markdown_file, tmp_path):
    """Test CLI with --output directory."""
    out_dir = tmp_path / "pdfs"
    out_dir.mkdir()
    result = runner.invoke(app, [str(markdown_file), "--output", str(out_dir)])
    assert result.exit_code == 0
    assert "PDF generated" in result.stdout
    assert any(out_dir.iterdir())


def test_cli_with_output_not_a_dir(markdown_file, tmp_path):
    """Test error when --output path is not a directory."""
    not_a_dir = tmp_path / "file.txt"
    not_a_dir.write_text("x")
    result = runner.invoke(app, [str(markdown_file), "--output", str(not_a_dir)])
    assert result.exit_code == 1
    assert "not a directory" in result.stdout.lower()


def test_cli_nonexistent_markdown():
    """Test error on nonexistent markdown file."""
    result = runner.invoke(app, ["/nonexistent/resume.md"])
    assert result.exit_code != 0
