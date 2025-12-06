# Pyresume

This is a python script to build a pdf resume based on a markdown file and some given css style.

This package is just for documentation purposes and generating my own resume, if you found yourself here, you are probably
lost...

## Credits

This code is just a wrapper for the work done by Julien Maupetit with [md2pdf](https://github.com/jmaupetit/md2pdf).

## Requirements

- Python
- UV
- Pre-commit
- Commitizen
- Weasyprint

## Instructions

Instructions for setup can be found in the [taskfile](./taskfile.yaml)

## Examples

To generate a resume:

1. Place your resume file in `./pyresume/assets` as `resume.md`
2. Select a style from [style folder](src/pyresume/assets/styles/) if none is selected defaults to [simple style](src/pyresume/assets/styles/simple-style.css)
3. Run the execution command from the examples below, like `make resume-simple`, or `uv run src/pyresume/cli.py -bar`
4. Find the pdf resume under [output folder](./output)

- Use uv, available style options are `-simple`, `-bar`, `-divider`

```shell
uv run src/pyresume/cli.py -simple
```

- Run with path to your own css style

```shell
uv run src/pyresume/cli.py --style {{path/to/user/style.css}}
```

- Run with path to your PDF file

```shell
uv run src/pyresume/cli.py --md {{path/to/user/file.md}}
```

### Tests

- Run all tests

```shell
uv run pytest
```
