# Git Conventions

## Commits

Use `cz commit` (commitizen) for guided commits.

Schema: `type(scope): message`
- **type:** `feat`, `fix`, `chore`, `docs`, `break`
- **scope:** optional, e.g., `feat(cli): add output flag`
- **message:** lowercase, imperative, max 50 chars (subject)

Examples:
```
feat(tui): add output directory picker
fix(convert): handle empty markdown files
chore: update dependencies
```

## Branches

- Work on feature branches (e.g., `chore/update-resume`)
- Main branch: production-ready code only
- Merge via PR after review

## Before Committing

```
task run          # Ruff + pytest + type check
```

Fails if tests fail or code doesn't format.
