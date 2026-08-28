"""Dev tool: valida el formato del CHANGELOG y que esté actualizado.

Uso:
    uv run python scripts/check_changelog.py                 # valida CHANGELOG.md
    uv run python scripts/check_changelog.py --staged       # además chequea que los
                                                            # cambios staged de src/ se
                                                            # reflejen en el changelog
    uv run python scripts/check_changelog.py --pr-base main # igual que --staged pero
                                                            # contra el diff de una rama

Fallos (exit code != 0):
    - El CHANGELOG está mal formado (sin `## [Unreleased]`, secciones
      desconocidas, versiones inválidas, secciones repetidas).
    - Con `--staged` o `--pr-base`, el diff toca `src/**` pero no actualizó
      el CHANGELOG.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"

_KNOWN_SECTIONS = {"Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"}
_HEADING_RE = re.compile(r"^## \[(?P<version>[^\]]+)\]")
_SECTION_RE = re.compile(r"^### (?P<name>[A-Za-z]+)$")
_VERSION_RE = re.compile(
    r"^v?\d+\.\d+\.\d+"
    r"(-(alpha|beta|rc)\.?\d+)?$|^Unreleased$"
)


def _parse_changelog(text: str) -> dict[str, list[str]]:
    releases: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            current = match.group("version")
            releases.setdefault(current, [])
            continue
        if current is not None:
            section_match = _SECTION_RE.match(line.strip())
            if section_match:
                section = section_match.group("name")
                if section not in _KNOWN_SECTIONS:
                    raise SystemExit(
                        f"CHANGELOG: sección desconocida '### {section}'"
                        f" (válidas: {', '.join(sorted(_KNOWN_SECTIONS))})."
                    )
                releases[current].append(section)
    return releases


def _validate(releases: dict[str, list[str]]) -> None:
    if "Unreleased" not in releases:
        raise SystemExit(
            "CHANGELOG: falta la sección '## [Unreleased]'. "
            "Registrá los cambios pendientes de release."
        )
    for version, sections in releases.items():
        if not _VERSION_RE.match(version):
            raise SystemExit(
                f"CHANGELOG: versión inválida '[{version}]'. "
                "Usá 'Unreleased' o SemVer (ej. '1.2.3' o '1.2.3-rc.1')."
            )
        if len(sections) != len(set(sections)):
            raise SystemExit(f"CHANGELOG: sección repetida dentro de '[{version}]'.")


def _git(args: list[str]) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        return None
    return result.stdout.splitlines()


def _diff_files(base: str | None, staged: bool) -> list[str] | None:
    if staged:
        return _git(["diff", "--cached", "--name-only"])
    if base is None:
        return None
    merge_base = _git(["merge-base", base, "HEAD"])
    if not merge_base:
        return None
    return _git(["diff", "--name-only", merge_base[0], "HEAD"])


def _diff_touches_src(files: list[str] | None) -> bool:
    if files is None:
        return False
    touched_src = any(line.startswith("src/") for line in files)
    touched_changelog = any(line == "CHANGELOG.md" for line in files)
    return touched_src and not touched_changelog


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Chequear los cambios staged (índice) en lugar del diff de una rama.",
    )
    parser.add_argument(
        "--pr-base",
        default=None,
        help="Rama base para detectar si el PR toca src/ sin actualizar el CHANGELOG.",
    )
    args = parser.parse_args()

    text = CHANGELOG.read_text(encoding="utf-8")
    releases = _parse_changelog(text)
    _validate(releases)

    files = _diff_files(args.pr_base, args.staged)
    if _diff_touches_src(files):
        raise SystemExit(
            "CHANGELOG: el diff toca src/** pero no actualizó CHANGELOG.md. "
            "Agregá una entrada bajo '## [Unreleased]'."
        )
    print("CHANGELOG OK")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
