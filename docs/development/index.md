# Development






## To TestPyPI

Changed pyproject.toml
```toml
[project]
name="TUtils-cli"


# Add
[tool.hatch.build.targets.wheel]
packages = ["tutils"]
```
build
```bash
python -m build
```

```bash
twine upload --repository testpypi dist/*
```

## To PyPI

Changed to back
```toml
name="TUtils"


# Delete
[tool.hatch.build.targets.wheel]
packages = ["tutils"]
```
Rebuild
```bash
python -m build
```

```bash
twine upload dist/*
```