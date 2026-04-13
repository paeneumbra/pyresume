"""Markdown to PDF conversion pipeline."""

from datetime import datetime
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

TIMESTAMP_FMT = "%Y%m%d%H%M%S"


def markdown_to_html(markdown_path: Path) -> str:
    """Convert markdown file to HTML string."""
    with open(markdown_path, encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(md_content, extensions=["extra"])

    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
</head>
<body>
{html_body}
</body>
</html>"""

    return html_document


def generate_pdf(
    markdown_path: Path,
    css_path: Path | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Convert markdown to PDF with optional CSS styling.

    Args:
        markdown_path: Path to markdown resume file
        css_path: Path to CSS stylesheet (optional)
        output_dir: Directory for the generated PDF; defaults to CWD

    Returns:
        Path to generated PDF

    Raises:
        FileNotFoundError: If markdown file doesn't exist
        ValueError: If markdown file is empty
    """
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    if markdown_path.stat().st_size == 0:
        raise ValueError(f"Markdown file is empty: {markdown_path}")

    directory = output_dir if output_dir is not None else Path.cwd()
    timestamp = datetime.now().strftime(TIMESTAMP_FMT)
    output_path = directory / f"{markdown_path.stem}_{timestamp}.pdf"

    html_content = markdown_to_html(markdown_path)
    html = HTML(string=html_content)

    stylesheets = []
    if css_path and css_path.exists():
        stylesheets.append(CSS(filename=str(css_path)))

    html.write_pdf(str(output_path), stylesheets=stylesheets)

    return output_path
