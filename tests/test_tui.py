"""Tests for TUI module."""

import pytest

from pyresume.tui import find_markdown_files, find_output_dirs


def test_find_output_dirs_includes_cwd(tmp_path, monkeypatch):
    """Test that CWD is always included as first option."""
    monkeypatch.chdir(tmp_path)
    dirs = find_output_dirs()
    assert tmp_path in dirs
    assert dirs[0] == tmp_path


@pytest.mark.parametrize(
    "dir_name,should_include",
    [
        ("output", True),
        ("results", True),
        ("pdfs", True),
        (".hidden", False),
        (".venv", False),
        ("venv", False),
        ("tests", False),
        ("__pycache__", False),
    ],
)
def test_find_output_dirs_directory_filtering(
    tmp_path, monkeypatch, dir_name, should_include
):
    """Test that output dirs are included/excluded correctly."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / dir_name).mkdir()
    dirs = find_output_dirs()
    dir_path = tmp_path / dir_name
    if should_include:
        assert dir_path in dirs
    else:
        assert dir_path not in dirs


def test_find_output_dirs_recursive_subdirs(tmp_path, monkeypatch):
    """Test that nested subdirectories are discovered."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output" / "nested" / "deep").mkdir(parents=True)
    (tmp_path / "results").mkdir()
    dirs = find_output_dirs()
    assert tmp_path / "output" in dirs
    assert tmp_path / "output" / "nested" in dirs
    assert tmp_path / "output" / "nested" / "deep" in dirs
    assert tmp_path / "results" in dirs


@pytest.mark.parametrize(
    "file_name,should_include",
    [
        ("resume.md", True),
        ("my-cv.md", True),
        ("notes.md", True),
        ("README.md", False),
        ("readme.md", False),
        ("CHANGELOG.md", False),
        ("changelog.md", False),
        ("TODO.md", False),
        ("todo.md", False),
    ],
)
def test_find_markdown_files_file_filtering(
    tmp_path, monkeypatch, file_name, should_include
):
    """Test that markdown files are included/excluded correctly."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / file_name).write_text("# Content")
    files = find_markdown_files()
    file_path = tmp_path / file_name
    if should_include:
        assert file_path in files
    else:
        assert file_path not in files
