"""Command-line interface using Typer."""

from pathlib import Path

import typer

from pyresume.convert import generate_pdf
from pyresume.themes import list_themes, resolve_css

app = typer.Typer(
    help="Convert markdown resume to PDF with customizable CSS themes.",
    no_args_is_help=False,
)


@app.command()
def main(
    markdown: Path | None = typer.Argument(
        None,
        help="Path to markdown resume file",
        exists=True,
    ),
    minimal: bool = typer.Option(
        False,
        "--minimal",
        help="Use minimal theme",
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        help="Use clean theme",
    ),
    slate: bool = typer.Option(
        False,
        "--slate",
        help="Use slate theme",
    ),
    css: str | None = typer.Option(
        None,
        "--css",
        help="Path to custom CSS file",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for generated PDF (defaults to current directory)",
    ),
    list_available: bool = typer.Option(
        False,
        "--list",
        help="List available themes and exit",
    ),
) -> None:
    """Convert markdown resume to PDF with customizable CSS themes."""
    if list_available:
        typer.echo("Available themes:")
        for theme in list_themes():
            typer.echo(f"  - {theme}")
        raise typer.Exit()

    # If no markdown provided, launch TUI
    if markdown is None:
        from pyresume.tui import run_tui

        run_tui()
        return

    # Determine which theme flag was set
    theme_flags = [minimal, clean, slate]
    theme_names = ["minimal", "clean", "slate"]
    active_themes = [name for flag, name in zip(theme_flags, theme_names) if flag]

    if len(active_themes) > 1:
        typer.echo(
            typer.style(
                "Error: Only one theme flag can be used at a time",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(1)

    if css and active_themes:
        typer.echo(
            typer.style(
                "Error: Cannot use both --css and a theme flag",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(1)

    if output is not None and not output.is_dir():
        typer.echo(
            typer.style(
                f"Error: Output path is not a directory: {output}", fg=typer.colors.RED
            )
        )
        raise typer.Exit(1)

    # Resolve CSS path
    theme = active_themes[0] if active_themes else "clean"
    try:
        css_path = resolve_css(theme=theme if not css else None, css_path=css)
    except (ValueError, FileNotFoundError) as e:
        typer.echo(typer.style(f"Error: {e}", fg=typer.colors.RED))
        raise typer.Exit(1)

    # Generate PDF
    try:
        result = generate_pdf(
            markdown_path=markdown,
            css_path=css_path,
            output_dir=output,
        )
        typer.echo(
            typer.style(
                f"✓ PDF generated: {result}",
                fg=typer.colors.GREEN,
            )
        )
    except (FileNotFoundError, ValueError) as e:
        typer.echo(typer.style(f"Error: {e}", fg=typer.colors.RED))
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(
            typer.style(
                f"Error: Failed to generate PDF: {e}",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
