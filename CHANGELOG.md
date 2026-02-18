# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `ScriptManager.fuzzy_search()`: fuzzy search scripts by name using `difflib.SequenceMatcher`, matches only against the script name part (after the dot)
- `script search` command: fuzzy search scripts with scored results table
- `script info` command: display detailed script information with `-d`/`-s`/`-r` options for description, source files, and entry point
- `run` command: fuzzy search fallback when exact script match is not found, suggests similar script names
- `tutils/exceptions.py`: custom exception hierarchy (`TUtilsError`, `ConfigError`, `RepositoryError`, `ScriptError` and subclasses)
- `tutils/repository/gitfetcher.py`: `GitFetcher` class to clone specific paths via git sparse-checkout without fetching the full repository
- `utils.is_url()`: validate whether a string is a well-formed http/https/ftp URL
- `utils.url_dirname()`: return the parent directory portion of a URL
- `utils.url_join()`: safely join URL path segments (ignores leading slashes in parts)
- `utils.download_file()`: download a remote file with a Rich progress bar; sends `Cache-Control: no-cache` headers to bypass CDN caching
- `utils.is_url_status_ok()`: check whether a URL responds with HTTP 200 (uses HEAD request)
- `utils.is_reachable()`: check TCP-level connectivity to a URL host
- `RepositoryModel.update_to_local()`: download remote repository index and all script files to the local path
- `repository update` command: implemented to pull remote repositories by name (or all remote repos if no name given)

### Fixed

- `list_repo_scripts` table missing row separators (`end_section`)
- First run build directories issue
- Empty repo print issue
- Sub script color output
- Typer version too lower error
- `RepositoryIndexFileModel` and `ScriptIndexFileModel`: `scripts`, `src`, `param` fields now coerce `null` YAML values to empty lists instead of raising a Pydantic validation error
- `Env.to_dict()`: stringify all values so `WORK_DIR` (a `Path` object) is correctly passed as a string in subprocess environment variables
- CLI usage documentation (`docs/cli-usage.md`) in GNU/Google style
- `repo` as hidden alias for `repository` subcommand
- `repository show` command to display scripts in a repository
- `repository clean` command to remove non-existent repositories
- `repository link` command to link a local repository to a remote URL
- `repository type` command to change repository source type (local/remote)
- `repository update` command now accepts optional repository names
- `script` subcommand group with callback
- `repository` default callback to list repos when no subcommand is given
- `list_repo_scripts` method in ScriptManager
- `version` command to show version information
- `show-script` command to list all scripts
- `run` command to run python scripts with streaming output, timeout and max-lines controls
- `repository add` command to add local or remote repositories
- `repository remove` command to remove repositories with optional file deletion
- Repository and script index file system (`index.yaml`)
- ScriptManager for managing repositories and scripts
- ProcessRunner for script execution with streaming output
- YAML-based configuration system with Pydantic models
- Rich console output with colored tables
- Documentation and examples
- MIT License

### Changed

- `ProcessRunner`: subprocess inherits terminal directly instead of piping, preserving rich color and formatting output
- Remove `--max-lines` option from `run` command
- Rename repository type `web` to `remote` across CLI, config and documentation
- Remove `app_name` from `AppConfig` string representation
- Improve repo table display: add row separators, prevent Name column from being squeezed
- Replace `typer.echo` with `rprint` for consistent Rich output
