# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `repo` as hidden alias for `repository` subcommand
- `repository show` command to display scripts in a repository
- `repository clean` command to remove non-existent repositories
- `script` subcommand group with callback
- `repository` default callback to list repos when no subcommand is given
- `list_repo_scripts` method in ScriptManager

- `version` command to show version information
- `show-script` command to list all scripts
- `run` command to run python scripts with streaming output, timeout and max-lines controls
- `repository add` command to add local or web repositories
- `repository remove` command to remove repositories with optional file deletion
- `repository update` command (placeholder for web repository sync)
- Repository and script index file system (`index.yaml`)
- ScriptManager for managing repositories and scripts
- ProcessRunner for script execution with streaming output
- YAML-based configuration system with Pydantic models
- Rich console output with colored tables
- Documentation and examples
- MIT License

### Changed

- Improve repo table display: add row separators, prevent Name column from being squeezed
- Replace `typer.echo` with `rprint` for consistent Rich output

### Fixed

- First run build directories issue
- Empty repo print issue
- Sub script color output
- Typer version too lower error
