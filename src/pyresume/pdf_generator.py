import sys
from pathlib import Path
from typing import Union

from md2pdf.core import md2pdf

from pyresume.file_operations import FileOperations
from pyresume.settings import ASSETS_DIR, OUTPUT_DIR


class PdfGenerator:
    """Handles PDF generation from markdown files with CSS styling"""

    def __init__(self):
        self.output_dir = Path(OUTPUT_DIR)
        self.assets_dir = Path(ASSETS_DIR)

        FileOperations.assert_directory_exists(self.assets_dir)
        FileOperations.assert_directory_exists(self.output_dir)

    @property
    def default_resume_file(self) -> str:
        """Default resume filename"""
        return "resume.md"

    @property
    def example_resume_file(self) -> str:
        """Example resume filename to use as fallback"""
        return "example-resume.md"

    @property
    def default_resume_path(self) -> Path:
        """Get path to default resume, falling back to example if needed"""
        primary_path = self.assets_dir / self.default_resume_file
        fallback_path = self.assets_dir / self.example_resume_file

        return fallback_path if not primary_path.exists() else primary_path

    def get_output_path(self, input_file: Union[str, Path]) -> Path:
        """Determine output path based on input file"""
        input_path = Path(input_file)

        if str(input_path) == str(self.default_resume_path):
            filename = FileOperations.build_timestamped_filename()
            return self.output_dir / filename

        return FileOperations.build_output_path(input_path)

    def generate_pdf(self, style_path: str, markdown_path: Union[str, Path]) -> Path:
        """Generate PDF file using a given style based on a markdown file"""
        FileOperations.assert_file_exists(style_path)
        FileOperations.assert_file_exists(markdown_path)

        output_path = self.get_output_path(markdown_path)

        try:
            md2pdf(
                str(output_path),
                md_file_path=str(markdown_path),
                css_file_path=str(style_path),
            )

            FileOperations.assert_file_exists(output_path)
            print(f"File created successfully: {output_path}")
            return output_path

        except Exception as e:
            raise ValueError(f"PDF generation failed: {e}")

    def to_pdf(self, style_path: str, markdown_path: Union[str, Path]) -> Path:
        """Generate PDF"""
        try:
            return self.generate_pdf(style_path, markdown_path)
        except (FileNotFoundError, ValueError) as err:
            print(f"Fatal error: {err}")
            print("Application was terminated gracefully...")
            sys.exit(1)
