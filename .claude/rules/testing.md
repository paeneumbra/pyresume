# Testing

## Structure

- **Unit tests:** `tests/test_*.py` (pytest)
- **Fixtures:** shared in `tests/conftest.py` or inline
- **Coverage target:** 80%+ (especially new code)

## Run Tests

```
task test                    # Via uv (recommended)
uv run pytest tests/         # Direct pytest
uv run pytest -v             # Verbose (see all test names)
uv run pytest tests/test_cli.py::test_cli_help  # Single test
```

## Rules

1. **Parameterize similar tests** — use `@pytest.mark.parametrize` to avoid duplication

```
@pytest.mark.parametrize("theme", ["minimal", "clean", "slate"])
def test_theme(theme):
    ...
```

2. **Use tmp_path fixture** for file operations (auto-cleanup)
3. **Test error paths** — not just happy path
4. **No integration test pollution** — each test is independent

## New Features

Write tests *first* when adding features. Tests guide the API.
