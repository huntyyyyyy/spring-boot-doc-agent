"""Ast-grep scanner errors (neutral of spring façade to avoid soft import cycles)."""


class AstGrepError(RuntimeError):
    """Raised when the ast-grep subprocess fails or returns unparseable output."""


class AstGrepNotFoundError(AstGrepError):
    """Raised when the ast-grep binary cannot be found."""
