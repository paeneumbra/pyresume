# Pyresume

A Python CLI to build a PDF resume from a Markdown file with customizable CSS themes.

This package is just for documentation purposes and generating my own resume, if you found yourself here, you are probably
lost...

## Requirements

- Python 3.13+
- UV
- Pre-commit
- Commitizen
- Weasyprint (requires system libraries — see note below)

## Instructions

Instructions for setup can be found in the [taskfile](./taskfile.yaml)

## Usage

### Interactive TUI

Run without arguments to launch the interactive wizard — it will let you pick a markdown file and theme:

```shell
pyresume
```

### CLI

Pass a markdown file directly to skip the wizard:

```shell
pyresume path/to/resume.md
```

Available theme flags: `--minimal` (default), `--clean`, `--slate`

```shell
pyresume path/to/resume.md --clean
```

Use a custom CSS file instead of a built-in theme:

```shell
pyresume path/to/resume.md --css path/to/style.css
```

List available built-in themes:

```shell
pyresume --list
```

The generated PDF is saved in the project root with a timestamp, e.g. `resume_20260410_120000.pdf`.

### Tests

```shell
uv run pytest
```

## Note

Weasyprint requires some system-level libraries (like Pango or cairo). If you run into an error on macOS, you might need `brew install weasyprint`; on Linux, `sudo apt install python3-weasyprint`.
