import argparse
import sys

from pyresume.css_styles import CssStyles
from pyresume.file_operations import FileOperations
from pyresume.pdf_generator import PdfGenerator
from pyresume.version import __version__


def build_parser():
    """Build argument parser"""

    parser = argparse.ArgumentParser(
        description="Generate a pdf resume from a markdown file"
    )
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-c",
        "--css",
        type=str,
        metavar="path/to/file.css",
        help="Path to CSS style file",
    )
    group.add_argument("-simple", action="store_true", help="Use simple style.")
    group.add_argument(
        "-bar",
        action="store_true",
        help="Use style with colored bar headers",
    )
    group.add_argument(
        "-divider",
        action="store_true",
        help="Use style with colored divider",
    )
    group.add_argument(
        "-l", "--list", action="store_true", help="List all available styles"
    )
    group.add_argument(
        "-r", "--remove", action="store_true", help="Remove all PDF files from output"
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="Print pyresume version"
    )

    parser.add_argument(
        "-m",
        "--md",
        type=str,
        metavar="path/to/markdown/file.md",
        help="Path to markdown resume file",
    )

    return parser


def handle_special_flags(args: argparse.Namespace):
    """Handle standalone operations"""
    if args.version:
        print(f"pyresume {__version__}")
        sys.exit(0)

    if args.list:
        CssStyles.print_styles()
        sys.exit(0)

    if args.remove:
        FileOperations.remove_pdf_files_from_output_dir()
        print("All files removed from output directory")
        sys.exit(0)


def handle_style(args: argparse.Namespace) -> str:
    """Determine CSS style"""

    css_styles = CssStyles()

    if args.css:
        return args.css
    if args.bar:
        return css_styles.bar_style
    if args.divider:
        return css_styles.divider_style
    if args.simple:
        return css_styles.simple_style

    print("No style argument provided. Defaulting to simple style.")
    return css_styles.simple_style


def main():
    parser = build_parser()
    args = parser.parse_args()

    handle_special_flags(args)

    pdf_generator = PdfGenerator()
    markdown_file = args.md or pdf_generator.default_resume_path
    css_style = handle_style(args)

    pdf_generator.to_pdf(css_style, markdown_file)


if __name__ == "__main__":
    main()
