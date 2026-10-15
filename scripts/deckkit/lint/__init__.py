from . import contrast, density, fonts, notes, numbers, overflow, placeholders, structure
from .common import blocking, severity_of, sort_findings

CHECKS = [structure, placeholders, overflow, contrast, fonts, density, numbers, notes]


def run_all(deck, scenes, theme):
    """Every check returns a list of `[Severity] slide N (layout): message` strings; empty means clean."""
    found = []
    for mod in CHECKS:
        found += mod.check(deck, scenes, theme)
    return sort_findings(found)


__all__ = ["run_all", "blocking", "severity_of", "CHECKS"]
