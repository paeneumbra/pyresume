"""Tests for convert module."""

import pytest

from pyresume.convert import generate_pdf, markdown_to_html


@pytest.fixture
def markdown_file(tmp_path):
    """Create a temporary markdown file."""
    md = tmp_path / "resume.md"
    md.write_text("# Test Resume\n\n## Experience\n\nSome experience.")
    return md


@pytest.fixture
def css_file(tmp_path):
    """Create a temporary CSS file."""
    css = tmp_path / "style.css"
    css.write_text("body { font-size: 10pt; }")
    return css


def test_markdown_to_html_reads_file(markdown_file):
    """Test that markdown_to_html reads from file."""
    html = markdown_to_html(markdown_file)
    assert "<!DOCTYPE html>" in html
    assert "<h1>Test Resume</h1>" in html
    assert "Experience" in html


def test_generate_pdf_nonexistent_file(tmp_path):
    """Test error on nonexistent markdown file."""
    with pytest.raises(FileNotFoundError):
        generate_pdf(tmp_path / "nonexistent.md")


def test_generate_pdf_empty_file(tmp_path):
    """Test error on empty markdown file."""
    empty = tmp_path / "empty.md"
    empty.touch()
    with pytest.raises(ValueError):
        generate_pdf(empty)


def test_generate_pdf_creates_file(markdown_file, css_file, tmp_path):
    """Test that generate_pdf creates a PDF file."""
    result = generate_pdf(markdown_file, css_file, output_dir=tmp_path)
    assert result.parent == tmp_path
    assert result.stem.startswith(markdown_file.stem)
    assert result.suffix == ".pdf"
    assert result.stat().st_size > 0


def test_generate_pdf_without_css(markdown_file, tmp_path):
    """Test PDF generation without CSS file."""
    result = generate_pdf(markdown_file, css_path=None, output_dir=tmp_path)
    assert result.exists()


def test_generate_pdf_default_output_path(markdown_file, tmp_path, monkeypatch):
    """Test default output path uses CWD with timestamp."""
    monkeypatch.chdir(tmp_path)
    result = generate_pdf(markdown_file)
    try:
        assert result.parent == tmp_path
        assert result.stem.startswith(markdown_file.stem)
        assert result.suffix == ".pdf"
    finally:
        result.unlink(missing_ok=True)
