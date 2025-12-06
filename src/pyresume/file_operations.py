from datetime import datetime
from pathlib import Path
from typing import Union

from pyresume.settings import OUTPUT_DIR


class FileOperations:
    """Utilities for file and directory operations"""

    MARKDOWN_EXTENSIONS = {".md", ".markdown"}

    @staticmethod
    def assert_directory_exists(dir_path: Union[str, Path]) -> None:
        """Verify that the given path is an existing directory

        Args:
            dir_path: Path to directory to check

        Raises:
            FileNotFoundError: If path is not a directory
        """
        path = Path(dir_path)
        if not path.is_dir():
            raise FileNotFoundError(f"No directory was found at path: {path}")

    @staticmethod
    def assert_file_exists(file_path: Union[str, Path]) -> None:
        """Verify that the given path is an existing file

        Args:
            file_path: Path to file to check

        Raises:
            FileNotFoundError: If path is not a file
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"No file was found at path: {path}")

    @classmethod
    def replace_extension_with_pdf(cls, filename: str) -> str:
        """Replace markdown extension with .pdf extension

        Args:
            filename: Name of file with markdown extension

        Returns:
            Filename with .pdf extension

        Raises:
            ValueError: If file doesn't have a markdown extension
        """
        path = Path(filename)
        file_extension = path.suffix.lower()

        if file_extension not in cls.MARKDOWN_EXTENSIONS:
            raise ValueError(
                f"File must be markdown type (.md or .markdown), found {file_extension}"
            )

        return path.stem + ".pdf"

    @classmethod
    def build_output_path(cls, path: Path) -> Path:
        """Build output path for PDF file

        Args:
            path: Input markdown file path

        Returns:
            Full path to output PDF file
        """
        pdf_filename = cls.replace_extension_with_pdf(path.name)
        return OUTPUT_DIR / pdf_filename

    @staticmethod
    def remove_pdf_files_from_output_dir() -> int:
        """Remove all PDF files from output directory

        Returns:
            Number of files removed
        """
        count = 0
        for pdf in OUTPUT_DIR.glob("*.pdf"):
            pdf.unlink(missing_ok=True)
            count += 1
        return count

    @staticmethod
    def build_timestamped_filename(prefix: str = "resume") -> str:
        """Create a filename with timestamp

        Args:
            prefix: Prefix for filename (default: "resume")

        Returns:
            Filename in format: {prefix}-{timestamp}.pdf

        Example:
            >>> build_timestamped_filename("resume")
            'resume-20241206143022.pdf'
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}-{timestamp}.pdf"
