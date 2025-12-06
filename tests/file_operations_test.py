from pathlib import Path

import pytest

from pyresume.file_operations import FileOperations
from pyresume.settings import PROJECT_ROOT, OUTPUT_DIR


class TestDirectoryValidation:
    """Test directory existence validation"""

    def test_successful_locate_dir(self):
        FileOperations.assert_directory_exists(OUTPUT_DIR)

    def test_failed_locate_dir(self):
        with pytest.raises(
            FileNotFoundError, match=r"No directory was found at path: some-folder"
        ):
            FileOperations.assert_directory_exists("some-folder")


class TestFileValidation:
    """Test file existence validation"""

    def test_successful_validate_file_exists(self):
        test_file = PROJECT_ROOT / "tests" / "data" / "test-markdown-file.md"
        FileOperations.assert_file_exists(test_file)

    def test_failed_validate_file_exists(self):
        with pytest.raises(
            FileNotFoundError, match=r"No file was found at path: some-name.markdown"
        ):
            FileOperations.assert_file_exists("some-name.markdown")


class TestMarkdownExtensionReplacement:
    """Test markdown to PDF extension conversion"""

    @pytest.mark.parametrize(
        "input_name,expected",
        [
            ("some-name.md", "some-name.pdf"),
            ("some-name.markdown", "some-name.pdf"),
        ],
    )
    def test_successful_replacement(self, input_name, expected):
        pdf_path = FileOperations.replace_extension_with_pdf(input_name)
        assert pdf_path == expected

    @pytest.mark.parametrize(
        "invalid_file",
        [
            "some-name.txt",
            "some-name.bak",
            "some-name.doc",
        ],
    )
    def test_failure_for_non_markdown_file(self, invalid_file):
        with pytest.raises(
            ValueError, match=r"File must be markdown type.*found \.\w+"
        ):
            FileOperations.replace_extension_with_pdf(invalid_file)


class TestBuildOutputPath:
    """Test PDF output path generation"""

    def test_successful_pdf_output_path(self):
        expected_path = OUTPUT_DIR / "some-name.pdf"
        pdf_path = FileOperations.build_output_path(Path("/test/data/some-name.md"))
        assert pdf_path == expected_path

    def test_failure_for_non_markdown_extension(self):
        with pytest.raises(
            ValueError, match=r"File must be markdown type.*found \.\w+"
        ):
            FileOperations.build_output_path(Path("some-name.bak"))


class TestPDFCleanup:
    """Test PDF file removal operations"""

    def test_remove_pdfs_from_output_dir(self):
        test_pdf = OUTPUT_DIR / "test-file.pdf"
        test_pdf.touch()
        assert test_pdf.exists(), "Test PDF was not created"

        FileOperations.remove_pdf_files_from_output_dir()

        remaining_pdfs = list(OUTPUT_DIR.glob("*.pdf"))
        assert len(remaining_pdfs) == 0, (
            f"Found {len(remaining_pdfs)} PDFs after removal"
        )

    def test_remove_pdfs_when_directory_empty(self):
        # Should not raise error when no PDFs exist
        FileOperations.remove_pdf_files_from_output_dir()
        assert True
