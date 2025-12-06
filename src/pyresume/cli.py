import argparse
import sys
from pathlib import Path

from pyresume.css_styles import CssStyles
from pyresume.file_operations import FileOperations
from pyresume.pdf_generator import PdfGenerator
from pyresume.version import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser"""

    parser = argparse.ArgumentParser(
        prog="pyresume",
        description="Generate a PDF resume from a markdown file",
    )

    # Style options (mutually exclusive)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--css", type=Path, metavar="FILE", help="path to custom CSS style file"
    )
    group.add_argument(
        "-simple", action="store_true", help="use simple style (default)"
    )
    group.add_argument(
        "-bar", action="store_true", help="use style with colored bar headers"
    )
    group.add_argument(
        "-divider", action="store_true", help="use style with colored divider"
    )

    # Utility options (mutually exclusive with styles)
    group.add_argument(
        "-l", "--list", action="store_true", help="list all available styles"
    )
    group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="remove all PDF files from output directory",
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="show version and exit"
    )

    # Input markdown file
    parser.add_argument(
        "-m", "--md", type=Path, metavar="FILE", help="path to markdown resume file"
    )

    return parser


def handle_special_flags(args: argparse.Namespace) -> None:
    """Handle standalone operations that exit immediately"""
    if args.version:
        print(f"pyresume {__version__}")
        sys.exit(0)

    if args.list:
        CssStyles.print_styles()
        sys.exit(0)

    if args.remove:
        files_removed = FileOperations.remove_pdf_files_from_output_dir()
        print(
            f"All PDF files removed from output directory - removed {files_removed} files"
        )
        sys.exit(0)


def handle_style(args: argparse.Namespace) -> Path:
    """Determine which CSS style to use based on arguments

    Returns:
        Path to CSS file (either custom or built-in style)
    """
    css_styles = CssStyles()

    if args.css:
        return args.css
    if args.bar:
        return css_styles.bar_style
    if args.divider:
        return css_styles.divider_style
    if args.simple:
        return css_styles.simple_style

    print("No style specified. Using simple style.")
    return css_styles.simple_style


def main() -> None:
    """Main entry point for CLI"""
    parser = build_parser()
    args = parser.parse_args()

    handle_special_flags(args)

    pdf_generator = PdfGenerator()
    markdown_file = args.md or pdf_generator.default_resume_path
    css_style = handle_style(args)

    try:
        pdf_generator.to_pdf(css_style, markdown_file)
        print("✓ PDF generated successfully")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
