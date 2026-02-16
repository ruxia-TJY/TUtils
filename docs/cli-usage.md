# CLI Usage

## NAME

`tutils` - A command-line tool for managing and running script repositories.

## SYNOPSIS

```
tutils [--version | -v] [--help]
tutils <command> [<args>]
```

## DESCRIPTION

`tutils` provides a set of subcommands for running Python scripts, managing script repositories, and organizing automation workflows.

## GLOBAL OPTIONS

`--version`, `-v`
:   Print version information and exit.

`--help`
:   Print help message and exit.

## COMMANDS

### show-script

List all available scripts across all registered repositories.

```
tutils show-script
```

---

### run

Run a script with streaming output and process controls.

```
tutils run <script> [<args>...] [options]
```

#### Positional arguments

`<script>`
:   Path to a Python script, or a script name. If the path does not exist, `tutils` automatically searches all registered repositories for a matching script.

`<args>`
:   Arguments passed through to the script.

#### Options

`--timeout` *FLOAT*
:   Maximum execution time in seconds. The process is killed after this limit.

`--max-lines` *INT*
:   Maximum number of output lines. The process is stopped once this limit is reached.

`-d`, `--debug`
:   Enable debug mode. Prints additional diagnostic information after execution.

#### Examples

```bash
# Run a local script
tutils run ./my_script.py

# Run a script from a repository with arguments
tutils run tcount :--show

# Run a script from a specific repository
tutils run File.tcount

# Set a 30-second timeout and cap output at 100 lines
tutils run tcount --timeout 30 --max-lines 100

# Run in debug mode
tutils run tcount -d
```

---

### repository (repo)

Manage script repositories. When invoked without a subcommand, lists all registered repositories.

```
tutils repository
tutils repository <subcommand> [<args>]
```

> `repo` is a shorthand alias for `repository`.

#### repository show

Display all scripts in a given repository.

```
tutils repository show <repo_name>
```

`<repo_name>`
:   Name of the repository to inspect.

#### repository add

Register a new repository.

```
tutils repository add <path> <name> [--type local|web] [<link>]
```

`<path>`
:   Directory path of the repository. Supports relative paths, absolute paths, and names.

`<name>`
:   A unique name for the repository.

`-t`, `--type` *{local,web}*
:   Repository source type. Defaults to `local`.

`<link>`
:   Remote repository URL. Required when `--type` is `web`.

**Examples:**

```bash
# Add a local repository
tutils repository add ./my-scripts my-repo

# Add a remote repository
tutils repository add ./my-scripts my-repo --type web https://github.com/user/repo

# Add by name, will be created under ~/.tutils/Scripts/
tutils repository add File File
```

#### repository remove

Remove one or more repositories from the configuration.

```
tutils repository remove <repo_name>... [-d | --delete]
```

`<repo_name>...`
:   One or more repository names to remove.

`-d`, `--delete`
:   Also delete repository files from disk.

**Examples:**

```bash
# Remove from config only
tutils repository remove my-repo

# Remove from config and delete files
tutils repository remove my-repo --delete

# Remove multiple repositories
tutils repository remove repo1 repo2
```

#### repository clean

Remove stale entries whose paths no longer exist on disk.

```
tutils repository clean
```

#### repository update

Pull updates for remote repositories. *(Under development)*

```
tutils repository update
```

---

### script

Manage scripts. When invoked without a subcommand, displays help.

> TODO: Implement query, display repository info, and other commands.

---

## FILES

`~/.tutils/`
:   Configuration root directory.

`~/.tutils/Scripts/`
:   Script storage directory.

`~/.tutils/Scripts/default/`
:   Default repository directory.

## SEE ALSO

- [Quick Start](quickstart.md)
- [Installation](installation.md)
- Report bugs: <https://github.com/ruxia-TJY/TUtils/issues>