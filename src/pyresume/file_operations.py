from datetime import datetime
from pathlib import Path

from pyresume.settings import OUTPUT_DIR


class FileOperations:
    @staticmethod
    def assert_directory_exists(dir_path):
        """Check if the given path is a directory"""
        path = Path(dir_path)
        if not path.is_dir():
            raise FileNotFoundError(f"No directory was found at path: {path}")

    @staticmethod
    def assert_file_exists(file_path):
        """Check if the given path is a file, if not raise an exception"""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"No file was found at path: {path}")

    @staticmethod
    def replace_extensions_markdown_for_pdf(filename: str):
        """Replace markdown for pdf extension, if file extension is not markdown raise an error"""
        file_extension = Path(filename).suffix
        if file_extension in [".md", ".markdown"]:
            return filename.replace(file_extension, ".pdf")
        else:
            raise ValueError(
                f"File must be from type markdown, instead {file_extension} was found"
            )

    @classmethod
    def build_output_path(cls, path: Path) -> Path:
        """Build new filename for pdf file"""
        pdf_filename = cls.replace_extensions_markdown_for_pdf(path.name)
        return OUTPUT_DIR / pdf_filename

    @staticmethod
    def remove_pdf_files_from_output_dir():
        """Remove PDF files from output dir if some exist"""
        for pdf in OUTPUT_DIR.glob("*.pdf"):
            pdf.unlink()

    @staticmethod
    def build_timestamped_filename(prefix: str = "resume") -> str:
        """Create a filename with timestamp identifier"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}-{timestamp}.pdf"
