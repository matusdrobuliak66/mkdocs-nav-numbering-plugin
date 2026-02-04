# Release checklist

1. Update version in pyproject.toml
2. Update README.md if needed
3. Run tests/build locally: `python -m build`
4. Commit changes and push
5. Create a GitHub Release (tag vX.Y.Z)
6. GitHub Actions will publish to PyPI

Notes:
- Publishing uses OIDC via GitHub Actions (no API token required)
- Ensure the package name is reserved on PyPI
