# Code Style

## Automated

Ruff enforces style. Run `task run` after edits.

- **Formatting:** `ruff format` (line length: auto via pyproject.toml)
- **Linting:** `ruff check --fix` (removes unused imports, enforces PEP 8)
- **Type checking:** `uv run ty check` (basic type hints)

## Manual Conventions

1. **Function naming:** snake_case; private functions prefixed with `_`

```
def _format_output_dir(path: Path, cwd: Path) -> str:
```

2. **Type hints:** Add for function params and returns

```
def find_markdown_files() -> list[Path]:
```

3. **Docstrings:** Only for public functions; describe WHAT and WHY, not HOW

```
def find_markdown_files() -> list[Path]:
    """Find markdown files under CWD, excluding hidden dirs and venv."""
```

4. **Comments:** Only for non-obvious logic (workarounds, constraints)
5. **No lambdas in assignments** — use `def` (E731)

```
def _format_output_dir(...):  # Not: output_dir_display = lambda ...
```

6. **DRY:** Extract duplicated logic into helper functions

## Constants

Use UPPERCASE for module-level constants:

```
EXCLUDED_FILES = {"readme.md", "changelog.md"}
```
