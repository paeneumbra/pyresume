"""InquirerPy-based TUI wizard for resume generation."""

from pathlib import Path

from InquirerPy import inquirer
from rich.console import Console
from rich.status import Status

from pyresume.convert import generate_pdf
from pyresume.themes import list_themes, resolve_css

console = Console()


def find_markdown_files() -> list[Path]:
    """Find all markdown files under CWD, excluding .venv, hidden dirs, and READMEs."""
    cwd = Path.cwd()
    return sorted(
        p
        for p in cwd.rglob("*.md")
        if p.name.lower() not in {"readme.md", "changelog.md"}
        and not any(
            part.startswith(".") or part in ("venv", ".venv")
            for part in p.relative_to(cwd).parts
        )
    )


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

    # Step 3: confirm
    console.print(f"\n  [dim]file[/]   {markdown_path.name}")
    console.print(f"  [dim]theme[/]  {theme}\n")

    confirmed: bool = inquirer.confirm(
        message="Generate PDF?",
        default=True,
    ).execute()

    if not confirmed:
        console.print("[dim]Cancelled.[/]")
        return

    # Step 4: generate
    with Status("Generating PDF…", console=console):
        try:
            css_path = resolve_css(theme=theme)
            output_path = generate_pdf(
                markdown_path=markdown_path,
                css_path=css_path,
            )
        except KeyboardInterrupt:
            raise
        except Exception as e:
            console.print(f"[red]Error:[/] {e}")
            return

    console.print(f"[green]✓[/] {output_path}")
