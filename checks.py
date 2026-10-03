"""Built-in rules for NPM/React/TypeScript projects."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator

from engine import ERROR, WARNING, INFO, check

# --------------------------------------------------------------------------
# NPM001: Missing Lockfile
# --------------------------------------------------------------------------

@check(id="NPM001", category="dependencies", severity=ERROR,
       description="Missing package-lock.json, yarn.lock, or pnpm-lock.yaml")
def missing_lockfile(path: Path, text: str) -> Iterator[tuple[int, str]]:
    """Checks if a lockfile exists in the project root."""
    if path.name != "package.json":
        return
        
    root = path.parent
    has_lock = (root / "package-lock.json").exists() or \
               (root / "yarn.lock").exists() or \
               (root / "pnpm-lock.yaml").exists()
               
    if not has_lock:
        yield 1, "No lockfile found. Always commit your package-lock.json, yarn.lock, or pnpm-lock.yaml."

# --------------------------------------------------------------------------
# NPM002: Exact versions in package.json
# --------------------------------------------------------------------------

@check(id="NPM002", category="dependencies", severity=WARNING, files="package.json",
       description="Dependencies should use exact versions, not ranges (^ or ~)")
def exact_versions(path: Path, text: str) -> Iterator[tuple[int, str]]:
    """Checks if package.json dependencies use exact versions."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        yield 1, "package.json is not valid JSON"
        return

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    for line_no, line in enumerate(text.splitlines(), 1):
        for dep, version in deps.items():
            if f'"{dep}"' in line and (version.startswith('^') or version.startswith('~')):
                yield line_no, f"Dependency '{dep}' uses a version range ({version}). Pin exact versions for reproducibility."


# --------------------------------------------------------------------------
# TS001: Usage of explicit 'any' type
# --------------------------------------------------------------------------
_ANY_TYPE_RE = re.compile(r":\s*any\b")

@check(id="TS001", category="typescript", severity=WARNING, files=("*.ts", "*.tsx"),
       description="Usage of explicit 'any' type in TypeScript")
def explicit_any(path: Path, text: str) -> Iterator[tuple[int, str]]:
    """Flags the usage of the 'any' type in TypeScript files."""
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("//"):
            continue
        if _ANY_TYPE_RE.search(line):
            yield line_no, "Explicit 'any' type found. Use a more specific type or 'unknown'."

# --------------------------------------------------------------------------
# RCT001: Large React Components
# --------------------------------------------------------------------------
@check(id="RCT001", category="react", severity=INFO, files=("*.tsx", "*.jsx"),
       description="React component file is too long")
def large_component(path: Path, text: str) -> Iterator[tuple[int, str]]:
    """Warns if a React component file is extremely long."""
    line_count = len(text.splitlines())
    if line_count > 300:
        yield 1, f"Component file is {line_count} lines long. Consider breaking it into smaller sub-components."

# --------------------------------------------------------------------------
# CFG001: Missing TypeScript config
# --------------------------------------------------------------------------
@check(id="CFG001", category="configuration", severity=ERROR,
       description="Missing tsconfig.json in a TypeScript project")
def missing_tsconfig(path: Path, text: str) -> Iterator[tuple[int, str]]:
    """If there are TS files, ensure tsconfig.json exists."""
    if not (path.name.endswith(".ts") or path.name.endswith(".tsx")):
        return
        
    if not (path.parent / "tsconfig.json").exists() and not (path.parent.parent / "tsconfig.json").exists():
        # Just yield once at line 1 of the TS file
        yield 1, f"Found TypeScript file '{path.name}', but no tsconfig.json was found in the project."

