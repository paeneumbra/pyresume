"""TUI wizard for resume generation."""

from pathlib import Path

from InquirerPy import inquirer
from rich.console import Console
from rich.status import Status

from pyresume.convert import generate_pdf
from pyresume.themes import list_themes, resolve_css

console = Console()

EXCLUDED_FILES = {"readme.md", "changelog.md", "todo.md"}
EXCLUDED_FOLDERS = {"venv", ".venv", "tests", "__pycache__"}


def _should_exclude_path(relative_parts: tuple[str, ...]) -> bool:
    """Check if path should be excluded from traversal."""
    return any(
        part.startswith(".") or part in EXCLUDED_FOLDERS for part in relative_parts
    )


def find_markdown_files() -> list[Path]:
    """Find markdown files under CWD, excluding hidden dirs, venv, and standard docs."""
    cwd = Path.cwd()
    return sorted(
        p
        for p in cwd.rglob("*.md")
        if p.name.lower() not in EXCLUDED_FILES
        and not _should_exclude_path(p.relative_to(cwd).parts)
    )


def _format_output_dir(path: Path, cwd: Path) -> str:
    """Format output directory path for display."""
    return "./" if path == cwd else str(path.relative_to(cwd))


def find_output_dirs() -> list[Path]:
    """Find available output directories under CWD, with CWD as first option."""
    cwd = Path.cwd()
    dirs = [cwd]
    try:
        for p in cwd.rglob("*/"):
            if not _should_exclude_path(p.relative_to(cwd).parts):
                dirs.append(p)
    except OSError:
        pass
    return sorted(set(dirs), key=lambda d: (d != cwd, str(d)))


def run_tui() -> None:
    """Run the interactive wizard."""

    # Step 1: pick markdown file from project list
    md_files = find_markdown_files()
    if not md_files:
        console.print("[red]No markdown files found in project.[/]")
        return

    cwd = Path.cwd()
    markdown_path: Path = inquirer.select(
        message="Resume file:",
        choices=[{"name": str(p.relative_to(cwd)), "value": p} for p in md_files],
    ).execute()

    # Step 2: pick theme
    theme: str = inquirer.select(
        message="Theme:",
        choices=list_themes(),
    ).execute()

    # Step 3: pick output directory
    output_dirs = find_output_dirs()
    output_dir: Path = inquirer.select(
        message="Output directory:",
        choices=[{"name": _format_output_dir(d, cwd), "value": d} for d in output_dirs],
    ).execute()

    # Step 4: confirm
    console.print(f"[dim]file[/] {markdown_path.name}")
    console.print(f"[dim]theme[/] {theme}")
    console.print(f"[dim]output[/] {_format_output_dir(output_dir, cwd)}")

    confirmed: bool = inquirer.confirm(
        message="Generate PDF?",
        default=True,
    ).execute()

    if not confirmed:
        console.print("[dim]Cancelled.[/]")
        return

    # Step 5: generate
    with Status("Generating PDF…", console=console):
        try:
            css_path = resolve_css(theme=theme)
            output_path = generate_pdf(
                markdown_path=markdown_path,
                css_path=css_path,
                output_dir=output_dir,
            )
        except KeyboardInterrupt:
            raise
        except Exception as e:
            console.print(f"[red]Error:[/] {e}")
            return

    console.print(f"[green]✓[/] {output_path}")
