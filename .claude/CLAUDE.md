# Pyresume

Python 3.13+ CLI: convert markdown resumes to PDF with CSS themes.

## Tech Stack

- **CLI:** Typer (type-safe Python CLIs)
- **TUI:** InquirerPy + Rich (interactive wizard)
- **PDF:** Weasyprint + markdown lib (CSS-driven rendering)
- **Package manager:** UV (lock file, fast sync)
- **Linting:** Ruff (check + format via `prek`)
- **Testing:** pytest (unit tests in `tests/`, fixtures in conftest)
- **Commits:** commitizen (conventional commits via `cz`)

## Run Locally

```bash
# Install deps & sync venv
task setup

# Run interactive wizard
pyresume

# Convert file with theme
pyresume path/to/resume.md --clean

# List themes
pyresume --list
```

## Testing

```bash
task test         # Run pytest via uv
uv run pytest     # Direct pytest
```

Tests parameterized by theme; adding a theme auto-tests all variants.

## Linting & Formatting

```bash
task run          # Run prek (ruff check, ruff format, type check, tests)
```

Do this after implementations. Ruff auto-fixes most style issues.

## Conventions

- **Commits:** `feat(scope): message`, `fix(scope):`, `chore:`, `docs:`
- **Branch:** greenfield (feature branch)
- **Modules:** `cli.py` (Typer app), `tui.py` (wizard), `convert.py` (PDF pipeline), `themes.py` (CSS resolution)
- **Private functions:** prefixed with `_` (e.g., `_format_output_dir`)

## Constraints

- **No external resume assets:** Only built-in themes (minimal, clean, slate)
- **PDF output:** Default to CWD with timestamp `YYYYMMDDHHMMSS`
- **Excluded files:** README.md, CHANGELOG.md, TODO.md (TUI scanner)
- **Excluded dirs:** .venv, venv, tests, **pycache**, hidden (startswith `.`)
