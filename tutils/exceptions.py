"""Custom exceptions for TUtils."""


class TUtilsError(Exception):
    """Base exception for all TUtils errors."""


# ── Config ──────────────────────────────────────────────────────────────────

class ConfigError(TUtilsError):
    """Base exception for configuration errors."""

class ConfigNotFoundError(ConfigError):
    """Raised when a config file does not exist."""

class ConfigFormatError(ConfigError):
    """Raised when a config file format is unsupported."""

class ConfigNotInitializedError(ConfigError):
    """Raised when the config manager has not been initialized."""


# ── Repository ───────────────────────────────────────────────────────────────

class RepositoryError(TUtilsError):
    """Base exception for repository errors."""

class RepositoryNotFoundError(RepositoryError):
    """Raised when a repository cannot be found."""

class RepositoryLocalPathNotExistError(RepositoryError):
    """Raised when a repository local path cannot be found."""

class RepositoryInvalidLinkError(RepositoryError):
    """Raised when a repository link is not a valid URL."""

class RepositoryConnnectFailedError(RepositoryError):
    """Raised when a repository connection fails."""

# ── Script ───────────────────────────────────────────────────────────────────

class ScriptError(TUtilsError):
    """Base exception for script errors."""

class ScriptNotFoundError(ScriptError):
    """Raised when a script cannot be found."""

