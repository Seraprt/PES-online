#!/usr/bin/env python3
"""Architecture conformance checker for PES Online Evolution.

Phase 1 gate. Validates that the repository matches the architecture:
required directories and files exist and are non-empty, .env.example exposes
every required key without duplicates, docker-compose declares PostgreSQL with
a healthcheck, .gitignore protects secrets, no source file contains a
placeholder marker, and the Makefile exposes the documented targets.

Exit code 0 = conformant, 1 = violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = (
    "apps",
    "packages",
    "infra",
    "docs",
    "docs/adr",
    "tools",
    ".github/workflows",
)

REQUIRED_FILES = (
    "README.md",
    "CHANGELOG.md",
    ".gitignore",
    ".editorconfig",
    ".gitattributes",
    ".env.example",
    "docker-compose.yml",
    "Makefile",
    "docs/architecture.md",
    "docs/folder-structure.md",
    "docs/domain-model.md",
    "docs/api-surface.md",
    "docs/phase-plan.md",
    "docs/adr/0001-monorepo-layout.md",
    "docs/adr/0002-backend-stack.md",
    "docs/adr/0003-realtime-and-match-lifecycle.md",
    "docs/adr/0004-companion-trust-model.md",
    "tools/check_architecture.py",
    ".github/workflows/ci.yml",
)

REQUIRED_ENV_KEYS = (
    "APP_ENV",
    "API_HOST",
    "API_PORT",
    "API_BASE_URL",
    "WEB_BASE_URL",
    "CORS_ORIGINS",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "DATABASE_URL",
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN_TTL_MINUTES",
    "REFRESH_TOKEN_TTL_DAYS",
    "B2_KEY_ID",
    "B2_APP_KEY",
    "B2_BUCKET",
    "B2_ENDPOINT",
    "COMPANION_WS_URL",
)

PLACEHOLDER_TOKENS = (
    "TODO",
    "FIXME",
    "XXX",
    "coming soon",
    "not implemented",
    "lorem ipsum",
)

SOURCE_ROOTS = ("apps", "packages", "infra", "tools")
SOURCE_SUFFIXES = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".yml",
    ".yaml",
    ".toml",
    ".json",
    ".sh",
    ".sql",
    ".css",
    ".html",
    ".md",
}
SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "coverage",
}
MAKEFILE_TARGETS = ("help:", "env:", "up:", "down:", "check:", "verify:")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_required_dirs(errors: list[str]) -> None:
    for name in REQUIRED_DIRS:
        if not (ROOT / name).is_dir():
            errors.append(f"missing directory: {name}")


def check_required_files(errors: list[str]) -> None:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"missing file: {name}")
        elif path.stat().st_size == 0:
            errors.append(f"empty file: {name}")


def read_env_keys(path: Path) -> list[str]:
    keys: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        keys.append(line.split("=", 1)[0].strip())
    return keys


def check_env(errors: list[str]) -> None:
    path = ROOT / ".env.example"
    if not path.is_file():
        return
    keys = read_env_keys(path)
    seen: set[str] = set()
    for key in keys:
        if key in seen:
            errors.append(f".env.example duplicate key: {key}")
        seen.add(key)
    for key in REQUIRED_ENV_KEYS:
        if key not in seen:
            errors.append(f".env.example missing key: {key}")


def check_compose(errors: list[str]) -> None:
    path = ROOT / "docker-compose.yml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for needle in ("postgres:", "healthcheck:", "postgres_data:"):
        if needle not in text:
            errors.append(f"docker-compose.yml missing: {needle}")


def check_gitignore(errors: list[str]) -> None:
    path = ROOT / ".gitignore"
    if not path.is_file():
        return
    lines = {line.strip() for line in path.read_text(encoding="utf-8").splitlines()}
    if ".env" not in lines:
        errors.append(".gitignore must ignore .env")
    if "!.env.example" not in lines:
        errors.append(".gitignore must un-ignore .env.example")


def iter_source_files():
    self_path = Path(__file__).resolve()
    for root_name in SOURCE_ROOTS:
        root = ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.resolve() == self_path:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() in SOURCE_SUFFIXES:
                yield path


def check_placeholders(errors: list[str]) -> None:
    patterns = [re.compile(re.escape(token), re.IGNORECASE) for token in PLACEHOLDER_TOKENS]
    for path in iter_source_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                line = text[: match.start()].count("\n") + 1
                errors.append(
                    f"placeholder marker '{match.group(0)}' in {rel(path)}:{line}"
                )


def check_makefile(errors: list[str]) -> None:
    path = ROOT / "Makefile"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for target in MAKEFILE_TARGETS:
        if not re.search(rf"^{re.escape(target)}", text, re.MULTILINE):
            errors.append(f"Makefile missing target: {target}")


def main() -> int:
    errors: list[str] = []

    check_required_dirs(errors)
    check_required_files(errors)
    check_env(errors)
    check_compose(errors)
    check_gitignore(errors)
    check_placeholders(errors)
    check_makefile(errors)

    if errors:
        print(f"Architecture check failed ({len(errors)} violation(s)):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Architecture check passed:")
    print(f"  directories : {len(REQUIRED_DIRS)}")
    print(f"  files       : {len(REQUIRED_FILES)}")
    print(f"  env keys    : {len(REQUIRED_ENV_KEYS)}")
    print("  compose     : postgres service with healthcheck")
    print("  sources     : no placeholder markers")
    return 0


if __name__ == "__main__":
    sys.exit(main())